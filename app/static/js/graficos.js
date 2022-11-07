luxon.Settings.defaultLocale = "br";

function renderiza_grafico_peso(url){
    fetch(url, {
        method: 'get',
    }).then(function(result){
        return result.json()
    }).then(function(data){
        
        const ctx = document.getElementById('grafico_peso').getContext('2d');
        const myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.datas,
                datasets: [{
                    label: 'Peso',
                    data: data.pesos,
                    fill: false,
                    borderColor: '#1b5e20',
                    backgroundColor: '#1b5e20',
                    tension: 0.1,
                    borderWidth: 3,
                }]
            },
            options: {
                plugins: {
                  legend: {
                    position: 'none',
                  }
                },
                scales: {
                    x: {
                        type: "time",
                        time: {
                            tooltipFormat: 'd LLL y',
                            displayFormats: {
                                day: 'd LLL yy',
                                month: 'd LLL yy',
                            },
                        },
                        title: {
                            display: true,
                            text: 'Data'
                        },
                        adapters: {
                            date: {
                                locale: 'br',
                                zone: 'UTC'
                            }
                        },
                    },                   
                }
            }           
        });
    })
}

function renderiza_grafico_massa_muscular(url){
    fetch(url, {
        method: 'get',
    }).then(function(result){
        return result.json()
    }).then(function(data){
        
        const ctx = document.getElementById('grafico_massa_muscular').getContext('2d');
        const myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.datas,
                datasets: [{
                    label: 'Massa muscular',
                    data: data.massa_muscular,
                    fill: false,
                    borderColor: '#8bc34a',
                    backgroundColor: '#8bc34a',
                    tension: 0.1,
                    borderWidth: 3,
                }]
            },
            options: {    
                plugins: {
                  legend: {
                    position: 'none',
                  }
                },
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            tooltipFormat: 'd LLL y',
                            displayFormats: {
                                day: 'd LLL yy',
                                month: 'd LLL yy',
                            },
                        },
                        title: {
                            display: true,
                            text: 'Data'
                        },
                        adapters: {
                            date: {
                                locale: 'br',
                                zone: 'UTC'
                            }
                        },
                    },                   
                }
            }            
        });
    })
}

function renderiza_grafico_massa_gordura(url){
    fetch(url, {
        method: 'get',
    }).then(function(result){
        return result.json()
    }).then(function(data){
        
        const ctx = document.getElementById('grafico_massa_gordura').getContext('2d');
        const myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.datas,
                datasets: [{
                    label: 'Gordura',
                    data: data.massa_gordura,
                    fill: false,
                    borderColor: '#4caf50',
                    backgroundColor: '#4caf50',
                    tension: 0.1,
                    borderWidth: 3,
                }]
            },
            options: {
                plugins: {
                  legend: {
                    position: 'none',
                  }
                },
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            tooltipFormat: 'd LLL y',
                            displayFormats: {
                                day: 'd LLL yy',
                                month: 'd LLL yy',
                            },
                        },
                        title: {
                            display: true,
                            text: 'Data'
                        },
                        adapters: {
                            date: {
                                locale: 'br',
                                zone: 'UTC'
                            }
                        }
                    }
                }
            } 
        });
    })
}

function renderiza_grafico_imc(url){
    fetch(url, {
        method: 'get',
    }).then(function(result){
        return result.json()
    }).then(function(data){
        
        const ctx = document.getElementById('grafico_imc').getContext('2d');
        const myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.datas,
                datasets: [{
                    label: 'IMC',
                    data: data.imc,
                    fill: false,
                    borderColor: '#cddc39',
                    backgroundColor: '#cddc39',
                    tension: 0.1,
                    borderWidth: 3,
                }]
            },
            options: {
                plugins: {
                  legend: {
                    position: 'none',
                  }
                },
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            tooltipFormat: 'd LLL y',
                            displayFormats: {
                                day: 'd LLL yy',
                                month: 'd LLL yy',
                            },
                        },
                        title: {
                            display: true,
                            text: 'Data'
                        },
                        adapters: {
                            date: {
                                locale: 'br',
                                zone: 'UTC'
                            }
                        }
                    }
                }
            } 
        });
    })
}