document.addEventListener("DOMContentLoaded", () => {
  // Seletores
  const btnFiltrar = document.getElementById("btnFiltrar");
  const btnResetar = document.getElementById("btnResetar");
  const btnExportar = document.getElementById("btnExportar");
  const dataInicioEl = document.getElementById("dataInicio");
  const dataFimEl = document.getElementById("dataFim");
  const bancoFiltroEl = document.getElementById("bancoFiltro");
  const loading = document.getElementById("loading");

  const totalGastoEl = document.getElementById("totalGasto");
  const mesMaxEl = document.getElementById("mesMax");
  const bancoTopEl = document.getElementById("bancoTop");

  const ctxMes = document.getElementById("graficoMes").getContext("2d");
  const ctxBanco = document.getElementById("graficoBanco").getContext("2d");
  const ctxMesBanco = document.getElementById("graficoMesBanco").getContext("2d");
  const ctxMesPie = document.getElementById("graficoMesPie").getContext("2d");

  let chartMes = null;
  let chartBanco = null;
  let chartMesBanco = null;
  let chartMesPie = null;

  const BANCO_CORES = {
    "Itau": "#FF6200",
    "Bradesco": "#CC092F",
    "Santander": "#EC0000",
    "Nubank": "#8A05BE",
    "Outro": "#6c757d" // cinza padrão
  };

  function corBanco(banco) {
    return BANCO_CORES[banco] || BANCO_CORES["Outro"];
  }

  // Função para destruir chart existente
  function safeDestroy(chart) {
    if (chart) chart.destroy();
  }

  // Helpers
  const formatMesLabel = (yyyy_mm) => {
    if (!yyyy_mm) return "";
    const [y, m] = yyyy_mm.split("-");
    return `${m}/${y}`;
  };

  function agrupadoPorMes(gastos) {
    const mapa = {};
    gastos.forEach((g) => {
      const mes = g.mes.slice(0, 7); // pega YYYY-MM
      mapa[mes] = (mapa[mes] || 0) + Number(g.valor);
    });
    return mapa;
  }

  function agrupadoPorBanco(gastos) {
    const mapa = {};
    gastos.forEach((g) => {
      const b = g.banco || "Outro";
      mapa[b] = (mapa[b] || 0) + Number(g.valor);
    });
    return mapa;
  }

  function agrupadoMesBanco(gastos) {
    const mapa = {};
    gastos.forEach((g) => {
      const mes = g.mes.slice(0, 7); // pega YYYY-MM
      mapa[mes] = mapa[mes] || {};
      mapa[mes][g.banco] = (mapa[mes][g.banco] || 0) + Number(g.valor);
    });
    return mapa;
  }

  function atualizarResumo(gastos) {
    const total = gastos.reduce((s, g) => s + Number(g.valor), 0);
    totalGastoEl.innerText = total.toLocaleString("pt-BR", {
      style: "currency",
      currency: "BRL",
    });

    const porMes = agrupadoPorMes(gastos);
    const meses = Object.keys(porMes);
    if (meses.length === 0) {
      mesMaxEl.innerText = "-";
    } else {
      const topMes = meses.reduce((a, b) => (porMes[a] > porMes[b] ? a : b));
      mesMaxEl.innerText = `${formatMesLabel(topMes)} — ${porMes[topMes].toLocaleString(
        "pt-BR",
        { style: "currency", currency: "BRL" }
      )}`;
    }

    const porBanco = agrupadoPorBanco(gastos);
    const bancos = Object.keys(porBanco);
    if (bancos.length === 0) {
      bancoTopEl.innerText = "-";
    } else {
      const topBanco = bancos.reduce((a, b) => (porBanco[a] > porBanco[b] ? a : b));
      bancoTopEl.innerText = `${topBanco} — ${porBanco[topBanco].toLocaleString("pt-BR", {
        style: "currency",
        currency: "BRL",
      })}`;
    }
  }

  function renderGraficoMes(agregadoPorMes) {
    const labels = Object.keys(agregadoPorMes).sort();
    const data = labels.map((l) => agregadoPorMes[l]);

    safeDestroy(chartMes);
      chartMes = new Chart(ctxMes, {
      type: "line", // Linha do tempo
      data: {
        labels: labels.map(formatMesLabel),
        datasets: [{
          label: "Total gasto (R$)",
          data,
          borderColor: "#4e73df",
          backgroundColor: "rgba(78, 115, 223, 0.2)",
          fill: true,
          tension: 0.3
        }],
      },
      options: {
        responsive: true,
        plugins: { 
          title: { display: true, text: "Total de Gastos por Mês" } 
        },
        scales: { y: { beginAtZero: true } },
      },
    });
  }

  function renderGraficoMesBanco(agregadoMesBanco) {
    const meses = Object.keys(agregadoMesBanco).sort();
    const bancosSet = new Set();
    meses.forEach(m => Object.keys(agregadoMesBanco[m]).forEach(b => bancosSet.add(b)));
    const bancos = Array.from(bancosSet).sort();

    const datasets = bancos.map(banco => ({
    label: banco,
    data: meses.map(m => Number(agregadoMesBanco[m][banco] || 0)),
    backgroundColor: corBanco(banco),
    stack: "Stack 0",
    }));

    safeDestroy(chartMesBanco);
      chartMesBanco = new Chart(ctxMesBanco, {
      type: "bar",
      data: { labels: meses.map(formatMesLabel), datasets },
      options: {
        responsive: true,
        plugins: { 
          tooltip: { mode: "index", intersect: false },
          title: { display: true, text: "Gastos por Banco ao Longo do Tempo" } 
        },
        scales: { x: { stacked: true }, y: { stacked: true, beginAtZero: true } },
      },
    });
  }

  function renderGraficoBanco(agregadoPorBanco) {
    const labels = Object.keys(agregadoPorBanco);
    const data = labels.map((l) => agregadoPorBanco[l]);
    const backgroundColor = labels.map(corBanco);

    safeDestroy(chartBanco);
    chartBanco = new Chart(ctxBanco, {
      type: "pie",
      data: { labels, datasets: [{ data, backgroundColor }] },
      options: {
        responsive: true,
        plugins: { 
          title: { display: true, text: "Distribuição de Gastos por Banco" } 
        }
      },
    });
  }

  function renderGraficoMesPie(agregadoPorMes) {
    const labels = Object.keys(agregadoPorMes).map(formatMesLabel);
    const data = Object.keys(agregadoPorMes).map((l) => agregadoPorMes[l]);
    const backgroundColor = labels.map(() => `#${Math.floor(Math.random() * 16777215).toString(16)}`);

    if (chartMesPie) chartMesPie.destroy();

    chartMesPie = new Chart(ctxMesPie, {
      type: "pie",
      data: { labels, datasets: [{ data, backgroundColor }] },
      options: {
        responsive: true,
        plugins: {
          title: { display: true, text: "Distribuição de Gastos por Mês" }
        }
      },
    });
  }

  function atualizarGraficos(gastos) {
    atualizarResumo(gastos);
    renderGraficoMes(agrupadoPorMes(gastos));
    renderGraficoBanco(agrupadoPorBanco(gastos));
    renderGraficoMesPie(agrupadoPorMes(gastos));
    renderGraficoMesBanco(agrupadoMesBanco(gastos));
  }

  async function carregarDados(params = {}) {
    loading.style.display = "block";
    try {
      let gastos;
      if (!Object.keys(params).length && window.GASTOS_JSON) {
        gastos = window.GASTOS_JSON;
      } else {
        // Filtrar localmente por YYYY-MM
        gastos = window.GASTOS_JSON || [];
        const { data_inicio, data_fim, banco } = params;
        gastos = gastos.filter((g) => {
          const mes = g.mes.slice(0, 7);
          let dentroPeriodo = true;
          if (data_inicio) dentroPeriodo = dentroPeriodo && mes >= data_inicio;
          if (data_fim) dentroPeriodo = dentroPeriodo && mes <= data_fim;
          if (banco) dentroPeriodo = dentroPeriodo && g.banco === banco;
          return dentroPeriodo;
        });
      }
      gastos = gastos.map((g) => ({ ...g, valor: Number(g.valor) }));
      atualizarGraficos(gastos);
    } catch (err) {
      console.error(err);
    } finally {
      loading.style.display = "none";
    }
  }

  // Função para exportar os dados em csv
  function exportarCSV(gastos) {
    if (!gastos || gastos.length === 0) {
      alert("Não há dados para exportar.");
      return;
    }

    const headers = ["Mês", "Banco", "Valor", "Descrição"];
    const rows = gastos.map(g => [
      g.mes.slice(0,7),
      g.banco,
      g.valor.toFixed(2),
      g.descricao
    ]);

    let csvContent = [headers, ...rows].map(e => e.join(";")).join("\n");

    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.setAttribute("href", url);
    link.setAttribute("download", "gastos.csv");
    link.style.display = "none";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  // Eventos
  btnFiltrar.addEventListener("click", () => {
    const params = {
      data_inicio: dataInicioEl.value,
      data_fim: dataFimEl.value,
      banco: bancoFiltroEl.value,
    };
    carregarDados(params);
  });

  btnResetar.addEventListener("click", () => {
    dataInicioEl.value = "";
    dataFimEl.value = "";
    bancoFiltroEl.value = "";
    carregarDados();
  });

  btnExportar.addEventListener("click", () => {
    // Usa os mesmos filtros do carregarDados
    const params = {
      data_inicio: dataInicioEl.value,
      data_fim: dataFimEl.value,
      banco: bancoFiltroEl.value,
    };

    let gastos = window.GASTOS_JSON || [];
    gastos = gastos.filter((g) => {
      const mes = g.mes.slice(0, 7);
      let dentroPeriodo = true;
      if (params.data_inicio) dentroPeriodo = dentroPeriodo && mes >= params.data_inicio;
      if (params.data_fim) dentroPeriodo = dentroPeriodo && mes <= params.data_fim;
      if (params.banco) dentroPeriodo = dentroPeriodo && g.banco === params.banco;
      return dentroPeriodo;
    });

    exportarCSV(gastos);
  });

  // Inicial
  carregarDados();
});