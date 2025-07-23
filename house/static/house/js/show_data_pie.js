function pie_chart(data) {
    //初始化一个Echarts实例
    let myChart = echarts.init(document.getElementById('pie'));
    window.addEventListener('resize', function () {
        myChart.resize();
    });
    let houeTypeDom = document.getElementById("pie");
    let houeTypecharts = echarts.init(houeTypeDom);
    let houeTypeOption = {
        tooltip: {
            trigger: 'item',
            formatter:"{a} <br/>{b} : {c}({d}%)",
        },
        legend: {
            show: false
        },
        series: [
            {
                name: '户型占比',
                type: 'pie',
                radius: ['0%','50%'],
                center:['50%','60%'],
                labelLine:{
                    normal:{
                        show:true
                    },
                    emphasis:{
                        show:true
                    }
                },
                //饼状图内部名字
                label:{
                    normal:{
                        show:true
                    },
                    emphasis:{
                        show:true
                    }
                },
                 itemStyle: {
                    emphasis: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                },
                data: data
               
            }
        ]
    };

    houeTypeOption && houeTypecharts.setOption(houeTypeOption);

}