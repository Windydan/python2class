function get_line_data(data) {
    let myChart = echarts.init(document.getElementById('f_line'));
    window.addEventListener('resize', function () {
        myChart.resize();
    });

    // 组装回归分析用的二维数组 [ [index, 单价], ... ]
    let regressionData = [];
    for (let i = 0; i < data['avg_price'].length; i++) {
        if (data['avg_price'][i] !== null) {
            regressionData.push([i, data['avg_price'][i]]);
        }
    }

    // 回归分析
    var myRegression = ecStat.regression('linear', regressionData);

    // 组装ECharts用的散点数据
    let scatterData = [];
    for (let i = 0; i < data['avg_price'].length; i++) {
        if (data['avg_price'][i] !== null) {
            scatterData.push({
                value: [data['date_li'][i], data['avg_price'][i]]
            });
        }
    }
    // 组装回归线数据（x轴用日期）
    let regLine = myRegression.points.map(function (item, idx) {
        return [data['date_li'][item[0]], item[1]];
    });

    let option = {
        tooltip: {
            trigger: 'axis',
            formatter: function (params) {
                let str = params[0].axisValue + '<br>';
                params.forEach(function (item) {
                    let val = (item.data && item.data[1] != null) ? item.data[1].toFixed(2) : '-';
                    str += item.marker + item.seriesName + ': ' + val + '<br>';
                });
                return str;
            }
        },
        xAxis: {
            type: 'category',
            data: data['date_li'],
            name: '',
            boundaryGap: false
        },
        yAxis: {
            type: 'value',
            name: '平均价格/元',
            min: 1.5
        },
        series: [
            {
                name: '分散值(实际值)',
                type: 'scatter',
                data: scatterData,
                symbolSize: 10,
                itemStyle: { color: '#a94442' }
            },
            {
                name: '线性值(预测值)',
                type: 'line',
                data: regLine,
                showSymbol: false,
                itemStyle: { color: '#34495e' }
            }
        ]
    };

    myChart.setOption(option, true);
}