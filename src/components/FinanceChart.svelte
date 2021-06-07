<script>
    import Chart from 'chart.js/auto';
    import 'chartjs-adapter-luxon';
    import annotationPlugin from 'chartjs-plugin-annotation';
import Roller from './Roller.svelte';
    Chart.register(annotationPlugin);

    export let data;
    let canvas, chart, isInitialised = false, avgBuyPriceInitialised = false;

    $: if(data['buysOffers'].length > 0) {
        if (isInitialised) {
            chart.options.plugins.title.text = getTitle();
            chart.update();
        } else {
            drawPlot()
            isInitialised = true;
        }
    }

    $: if (data.avgBuyRate == null) {
        if(isInitialised)
            chart.options.plugins.annotation = {};
    } else {
        if(avgBuyPriceInitialised) {
            chart.options.plugins.annotation.annotations.avgBuyRate.value = data.avgBuyRate
        } else {
            if(isInitialised) {

                chart.options.plugins.annotation = {
                    annotations: {
                        avgBuyRate: {
                            type: 'line',
                            scaleID: 'y',
                            value: data.avgBuyRate,
                            borderColor: 'rgba(149, 165, 166, 1)',
                            borderWidth: 5,
                            borderDash: [10, 5],
                            label: {
                                content: () => `Avg buy rate: ${data.avgBuyRate} ${data['currencyPair'].split('-')[1]}`,
                                enabled: true
                            }
                        }
                    }
                }

                avgBuyPriceInitialised = true;
            }
        }
    }

    function getTitle() {
        return `${data['currencyPair']['isCandidate'] ? '✩' : ''} ${data['currencyPair']} ${data['trendSymbol']}`;
    }

    function drawPlot() {
        chart = new Chart(canvas, {
            data: {
                datasets: [{
                    label: 'Transaction',
                    type: 'line',
                    data: data['transactions'],
                    borderColor: 'rgba(0, 0, 255, 0.4)',
                    backgroundColor: 'rgba(0, 0, 255, 0.4)',
                },
                {   
                    label: 'Volume',
                    type: 'bar',
                    data: data['volumes'],
                    yAxisID: 'yVolume',
                    borderColor: 'rgba(103, 128, 159, 0.6)'
                },
                {
                    label: 'Best buy offer',
                    type: 'line',
                    data: data['buysOffers'],
                    borderColor: 'rgba(135, 211, 124, 1)',
                    backgroundColor: 'rgba(135, 211, 124, 1)',
                    pointRadius: 0
                },
                {
                    label: 'Best sell offer',
                    type: 'line',
                    data: data['sellsOffers'],
                    borderColor: 'rgba(240, 52, 52, 1)',
                    backgroundColor: 'rgba(240, 52, 52, 1)',
                    pointRadius: 0
                },
                {
                    label: 'RSI',
                    type: 'line',
                    data: data['rsi'],
                    yAxisID: 'yRSI',
                    borderColor: 'rgba(189, 195, 199, 1)',
                    backgroundColor: 'rgba(189, 195, 199, 1)',
                    borderDash: [10,5]
                }]
            },
            options: {
                legend: {
                    labels: {
                        defaultFontSize: 30
                    }
                },
                plugins: {
                    title: {
                        display: true,
                        // text: data['currencyPair'] + '⬆⬇✩[VA][LA]',
                        text: data['currencyPair'],
                        font: {
                            size: 18
                        }
                    },
                    // annotation: {
                    //     annotations: {
                    //         avgBuyPrice: {
                    //             type: 'line',
                    //             scaleID: 'yT',
                    //             value: 139500,
                    //             borderColor: 'rgb(255, 99, 132)',
                    //             borderWidth: 3,
                    //             label: {
                    //                 content: () => 'Your avg buy price is: 139500',
                    //                 enabled: true
                    //             }
                    //         }
                    //     }
                    // }
                },
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            minUnit: 'second',
                            stepSize: 2
                        },
                        ticks: {
                            source: 'auto',
                            maxRotation: 10,
                            autoSkip: true,
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: `Cena [${data['currencyPair'].split('-')[1]}]`,
                        }
                    },
                    yVolume: {
                        title: {
                            display: true,
                            text: `Volumen [${data['currencyPair'].split('-')[0]}]`
                        },
                        grid: {
                            display: false
                        }
                    },
                    yRSI: {
                        min: 0,
                        max: 100,
                        position: 'right',
                        title: {
                            display: true,
                            text: `RSI [${data['rsiPeriod']}]`
                        },
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
        canvas.style.visibility='visible';
    }
</script>

<div class='chartWrapper'>
    <div class='chart'>
        <canvas id='financeChart{data['id']}' width='3' height='1' bind:this={canvas} />
        {#if !isInitialised}
            <Roller />

            <h4>Loading {data['currencyPair']} chart, please wait...</h4>
        {/if }
    </div>
    <div class='profit'> 
        <b>Profit:</b>
        <br>
        {data['profit']} {data['currencyPair'].split('-')[1]}
    </div>
</div>

<style>
    .chartWrapper {
        display: inline-flex;
        width: 100%;
        margin: 20px;
    }

    .chartWrapper > .profit {
        flex: 1;
        margin: auto;
    } 

    div.profit {
        text-align: center;
    }

    .chartWrapper > .chart {
        flex: 5;
        margin: auto;
        text-align: center;
    } 

    canvas {
        background-color: white;
        visibility: hidden;
    }
</style>