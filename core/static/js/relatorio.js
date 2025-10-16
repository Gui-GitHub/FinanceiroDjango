document.addEventListener("DOMContentLoaded", () => {
  const gastos = window.GASTOS_JSON || [];
  const ganhos = window.GANHOS_JSON || [];

  const totalGastoEl = document.getElementById("totalGasto");
  const totalGanhoEl = document.getElementById("totalGanho");
  const saldoAtualEl = document.getElementById("saldoAtual");

  const btnFiltrar = document.getElementById("btnFiltrar");
  const btnResetar = document.getElementById("btnResetar");
  const btnExportar = document.getElementById("btnExportar");

  const dataInicio = document.getElementById("dataInicio");
  const dataFim = document.getElementById("dataFim");
  const bancoFiltro = document.getElementById("bancoFiltro");

  const loading = document.getElementById("loading");

  let chartInstances = [];

  // ======== FUNÇÕES AUXILIARES ===========
  function formatCurrency(value) {
    return value.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
  }

  function getMonthKey(dateStr) {
    const d = new Date(dateStr);
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}`;
  }

  function groupBy(arr, keyFn) {
    return arr.reduce((acc, item) => {
      const key = keyFn(item);
      acc[key] = acc[key] || [];
      acc[key].push(item);
      return acc;
    }, {});
  }

  function clearCharts() {
    chartInstances.forEach((chart) => chart.destroy());
    chartInstances = [];
  }

  // ======== PRINCIPAL ===========
  function atualizarRelatorio() {
    loading.style.display = "block";

    setTimeout(() => {
      const inicio = dataInicio.value ? new Date(dataInicio.value + "-01") : null;
      const fim = dataFim.value ? new Date(dataFim.value + "-01") : null;
      const banco = bancoFiltro.value;

      // FILTRAGEM
      const filtrar = (lista) =>
        lista.filter((item) => {
          const d = new Date(item.data);
          const bancoMatch = !banco || item.banco === banco;
          const dataMatch =
            (!inicio || d >= inicio) && (!fim || d <= new Date(fim.getFullYear(), fim.getMonth() + 1, 0));
          return bancoMatch && dataMatch;
        });

      const gastosFiltrados = filtrar(gastos);
      const ganhosFiltrados = filtrar(ganhos);

      const totalGasto = gastosFiltrados.reduce((sum, g) => sum + parseFloat(g.valor), 0);
      const totalGanho = ganhosFiltrados.reduce((sum, g) => sum + parseFloat(g.valor), 0);
      const saldoAtual = totalGanho - totalGasto;

      totalGastoEl.textContent = formatCurrency(totalGasto);
      totalGanhoEl.textContent = formatCurrency(totalGanho);
      saldoAtualEl.textContent = formatCurrency(saldoAtual);

      clearCharts();

      criarGraficoBanco(gastosFiltrados);
      criarGraficoGastoGanho(totalGasto, totalGanho);
      criarGraficoComparativoMes(gastosFiltrados, ganhosFiltrados);
      criarGraficoEvolucaoSaldo(gastosFiltrados, ganhosFiltrados);
      criarGraficoMesBanco(gastosFiltrados);

      loading.style.display = "none";
    }, 500);
  }

  // ======== GRÁFICOS ===========
  function criarGraficoBanco(gastosFiltrados) {
    const porBanco = groupBy(gastosFiltrados, (g) => g.banco || "Outro");
    const labels = Object.keys(porBanco);
    const valores = labels.map((b) => porBanco[b].reduce((sum, g) => sum + parseFloat(g.valor), 0));

    const ctx = document.getElementById("graficoBanco").getContext("2d");
    chartInstances.push(
      new Chart(ctx, {
        type: "bar",
        data: {
          labels,
          datasets: [{ label: "Total Gasto por Banco", data: valores }],
        },
        options: {
          responsive: true,
          plugins: {
            legend: { display: window.innerWidth > 768 }, // legenda só no desktop
            title: { 
              display: true, // sempre mostra título
              text: "Gastos por Banco", 
              font: { size: 18 } 
            },
          },
        },
      })
    );
  }

  function criarGraficoGastoGanho(totalGasto, totalGanho) {
    const ctx = document.getElementById("graficoGastoGanho").getContext("2d");
    chartInstances.push(
      new Chart(ctx, {
        type: "pie",
        data: {
          labels: ["Gastos", "Ganhos"],
          datasets: [{ data: [totalGasto, totalGanho], backgroundColor: ["#dc3545", "#198754"] }],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: window.innerWidth > 768, // legenda só no desktop
              position: "bottom"
            },
            title: { 
              display: true, // sempre mostra título
              text: "Proporção Gastos x Ganhos", 
              font: { size: 18 } 
            },
          },
        },
      })
    );
  }

  function criarGraficoComparativoMes(gastosFiltrados, ganhosFiltrados) {
    const gastosMes = groupBy(gastosFiltrados, (g) => getMonthKey(g.data));
    const ganhosMes = groupBy(ganhosFiltrados, (g) => getMonthKey(g.data));

    const meses = Array.from(new Set([...Object.keys(gastosMes), ...Object.keys(ganhosMes)])).sort();

    const totalGastos = meses.map((m) =>
      (gastosMes[m] || []).reduce((sum, g) => sum + parseFloat(g.valor), 0)
    );
    const totalGanhos = meses.map((m) =>
      (ganhosMes[m] || []).reduce((sum, g) => sum + parseFloat(g.valor), 0)
    );

    const ctx = document.getElementById("graficoComparativoMes").getContext("2d");
    chartInstances.push(
      new Chart(ctx, {
        type: "bar",
        data: { labels: meses, datasets: [{ label: "Gastos", data: totalGastos, backgroundColor: "#dc3545" }, { label: "Ganhos", data: totalGanhos, backgroundColor: "#198754" }] },
        options: {
          responsive: true,
          plugins: {
            legend: {
              display: window.innerWidth > 768, // legenda só no desktop
              position: "bottom"
            },
            title: { 
              display: true, // sempre mostra título
              text: "Comparativo Mensal Gastos x Ganhos", 
              font: { size: 18 } 
            },
          },
        },
      })
    );
  }

  function criarGraficoEvolucaoSaldo(gastosFiltrados, ganhosFiltrados) {
    const todos = [...gastosFiltrados.map((g) => ({ ...g, tipo: "gasto" })), ...ganhosFiltrados.map((g) => ({ ...g, tipo: "ganho" }))].sort((a, b) => new Date(a.data) - new Date(b.data));

    let saldo = 0;
    const labels = [];
    const valores = [];

    todos.forEach((item) => {
      saldo += item.tipo === "ganho" ? parseFloat(item.valor) : -parseFloat(item.valor);
      labels.push(item.data);
      valores.push(saldo);
    });

    const ctx = document.getElementById("graficoEvolucaoSaldo").getContext("2d");
    chartInstances.push(
      new Chart(ctx, {
        type: "line",
        data: { labels, datasets: [{ label: "Evolução do Saldo", data: valores, fill: false, borderColor: "#0d6efd", tension: 0.3 }] },
        options: {
          responsive: true,
          plugins: {
            legend: {
              display: window.innerWidth > 768, // legenda só no desktop
              position: "bottom"
            },
            title: { 
              display: true, // sempre mostra título
              text: "Evolução do Saldo ao Longo do Tempo", 
              font: { size: 18 } 
            },
          },
        },
      })
    );
  }

  function criarGraficoMesBanco(gastosFiltrados) {
    const bancos = Array.from(new Set(gastosFiltrados.map((g) => g.banco || "Outro")));
    const meses = Array.from(new Set(gastosFiltrados.map((g) => getMonthKey(g.data)))).sort();

    const datasets = bancos.map((banco) => {
      const data = meses.map((m) => {
        const filtrado = gastosFiltrados.filter((g) => g.banco === banco && getMonthKey(g.data) === m);
        return filtrado.reduce((sum, g) => sum + parseFloat(g.valor), 0);
      });
      return { label: banco, data };
    });

    const ctx = document.getElementById("graficoMesBanco").getContext("2d");
    chartInstances.push(
      new Chart(ctx, {
        type: "line",
        data: { labels: meses, datasets },
        options: {
          responsive: true,
          plugins: {
            legend: {
              display: window.innerWidth > 768, // legenda só no desktop
              position: "bottom"
            },
            title: { 
              display: true, // sempre mostra título
              text: "Gastos por Banco ao Longo do Mês", 
              font: { size: 18 } 
            },
          },
        },
      })
    );
  }

  // ======== EXPORTAÇÃO CSV ===========
  function exportarCSV() {
    const rows = [["Data", "Tipo", "Banco", "Valor"]];
    gastos.forEach((g) => rows.push([g.data, "Gasto", g.banco, g.valor]));
    ganhos.forEach((g) => rows.push([g.data, "Ganho", g.banco, g.valor]));

    let csvContent = "data:text/csv;charset=utf-8," + rows.map((e) => e.join(",")).join("\n");
    const link = document.createElement("a");
    link.setAttribute("href", encodeURI(csvContent));
    link.setAttribute("download", "relatorio_financeiro.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  // ======== EVENTOS ===========
  btnFiltrar.addEventListener("click", atualizarRelatorio);
  btnResetar.addEventListener("click", () => {
    dataInicio.value = "";
    dataFim.value = "";
    bancoFiltro.value = "";
    atualizarRelatorio();
  });
  btnExportar.addEventListener("click", exportarCSV);

  // ======== INICIALIZA ===========
  atualizarRelatorio();
});