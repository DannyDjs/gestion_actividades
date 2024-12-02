const ctx = document.getElementById('activityChart').getContext('2d');
    const activityChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ['Pendientes', 'En Proceso', 'Finalizadas'],
        datasets: [{
          data: [actividadesData.pendientes, 
            actividadesData.en_proceso, 
            actividadesData.finalizadas], 
          backgroundColor: ['#FFA726', '#A9A9A9', '#66BB6A'],
          hoverOffset: 10
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false, // Permite personalizar el tamaño sin distorsión
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                const label = context.label || '';
                const value = context.raw || 0;
                return `${label}: ${value} actividades`;
              }
            }
          }
        }
      }
    });

const ctxactividades = document.getElementById('actividadesChart').getContext('2d');
const actividadesChart = new Chart(ctxactividades, {
    type: 'bar',  // O usa 'pie' o 'doughnut' según lo prefieras
    data: {
        labels: tipoactividadesData.tipo_labels,  // Usa las etiquetas de tipo actividad
        datasets: [{
            label: 'Cantidad de Actividades',
            data: tipoactividadesData.actividad_counts,  // Usa los conteos de actividades
            backgroundColor: '#66BB6A',  // Color de las barras
            borderColor: '#388E3C',
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: true
            },
            tooltip: {
                callbacks: {
                    label: function(tooltipItem) {
                        return tooltipItem.label + ': ' + tooltipItem.raw + ' actividades';
                    }
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});   

const ctxInformesFirmados = document.getElementById('graficoInformesFirmados').getContext('2d');
const graficoInformesFirmados = new Chart(ctxInformesFirmados, {
    type: 'bar', // Tipo de gráfico
    data: {
        labels: informesfirmadosData.etiquetas_meses, // Etiquetas de los meses
        datasets: [{
            label: 'Informes Firmados',
            data: informesfirmadosData.datos_meses, // Datos de cada mes
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
        }]
    },
    options: {
        onClick: (event, elements) => {
          if (elements.length > 0) {
              const index = elements[0].index; // Índice de la barra clicada
              const mes = informesfirmadosData.etiquetas_meses[index]; // Mes seleccionado
              const informes = informesfirmadosData.informes_por_mes[mes]; // Informes de ese mes
          
              // Mostrar el modal con los datos de los informes
              mostrarModal(mes, informes);
          }
        },
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});


