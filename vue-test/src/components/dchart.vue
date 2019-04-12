<template lang='pug'>
  <div>
    vue-highcharts(:options="doptions" ref="lineCharts")
    button(@click="load") load-tokyo-dchart
  </div>
</template>

<script>
import VueHighcharts from 'vue2-highcharts'
import axios from 'axios'
const asyncData = {
  name: 'Tokyo',
  marker: {
    symbol: 'square'
  },
  data: [7.0, 6.9, 9.5, 14.5, 18.2, 21.5, 25.2, {
    y: 26.5,
    marker: {
      symbol: 'url(http://www.highcharts.com/demo/gfx/sun.png)'
    }
  }, 23.3, 18.3, 13.9, 9.6]
}
export default{
  components: {
    VueHighcharts
  },
  props: {
    doptions: Object,
    clickx: String,
    clicky: Number
  },
  data () {
    return {
      options: {
        chart: {
          type: 'spline',
          // type: 'pie',
          style: {
            fontFamily: '',
            fontSize: '12px',
            fontWeight: 'bold',
            color: '#006cee'
          },
          /* options3d: {
            enabled: true,
            alpha: 45,
            beta: 0
          }, */
          zoomType: 'x'
        },
        colors: ['#058DC7', '#50B432', '#ED561B', '#DDDF00', '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4'],
        title: {
          text: 'Monthly Average Temperature'
        },
        subtitle: {
          text: 'Source: WorldClimate.com'
        },
        xAxis: {
          title: {
            text: 'month'
          },
          categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        },
        yAxis: {
          title: {
            text: 'Temperature'
          },
          labels: {
            formatter: function () {
              return this.value + '°'
            }
          }
        },
        tooltip: {
          crosshairs: [true, true],
          shared: true
        },
        credits: {
          enabled: false
        },
        plotOptions: {
          spline: {
            marker: {
              radius: 4,
              lineColor: '#666666',
              lineWidth: 1
            }
          },
          /* pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            depth: 35,
            dataLabels: {
              enabled: true,
              format: '{point.name}'
            }
          }, */
          column: {
            colorByPoint: true
          }
          /* series: {
            colorByPoint: true
          } */
        },
        series: []
        /* series: [
          {
            'name': 'china',
            type: 'column',
            // type: 'pie',
            'data': [1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2]
            // 'data': []
            // 'data': [['a', 1], ['b', 2], ['c', 3], ['d', 4], ['e', 5], ['f', 6], ['g', 7], ['h', 6], ['i', 5], ['j', 4]]
          }
        ] */
      }
    }
  },
  mounted () {
    this.asyncgetvalue()
    // this.load()
  },
  methods: {
    load () {
      let lineCharts = this.$refs.lineCharts
      lineCharts.delegateMethod('showLoading', 'Loading...')
      setTimeout(() => {
        lineCharts.addSeries(asyncData)
        lineCharts.hideLoading()
      }, 2000)
    },
    getvalue () {
      let value = {
        'name': 'china',
        'type': 'column'
      }
      axios({
        method: 'get',
        url: 'http://localhost:9000/getvalue/'
        // data: JSON.stringify({check: 'checked', username: 'username'})
      }).then(response => {
        if (response.data.errno === '0') {
          console.log('ok')
          // value.data = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
          value.data = response.data.data
          let lineCharts = this.$refs.lineCharts
          lineCharts.addSeries(value)
        } else {
          console.log('err')
        }
      }).catch(function (error) {
        console.log(error)
      })
    },
    asyncgetvalue: async function () {
      let value = {
        'name': 'china',
        'type': 'column'
      }
      const response = await axios({
        method: 'get',
        // url: 'http://localhost:9000/getvalue/'
        url: '/getvalue/'
        // data: JSON.stringify({check: 'checked', username: 'username'})
      })
      if (response.data.errno === '0') {
        console.log('dchart async get value ok')
        value.data = response.data.data
        let lineCharts = this.$refs.lineCharts
        // console.log(this.clickx, this.clicky, lineCharts, this.doptions)
        lineCharts.addSeries(value)
      } else {
        console.log('err')
      }
    }
  }
}
</script>
