import { Chart, useChart } from "@chakra-ui/charts"
import { Text } from "@chakra-ui/react";
import { CartesianGrid, Line, LineChart, Tooltip, XAxis, YAxis } from "recharts"

// movies watched per year-month line chart

function YMLine({stats}){

    const chartData = Object.entries(stats.movies_per_year_month).map(
        ([month_year, count]) => ({
            name: month_year,
            value: count
        })
    )

    // Sort data by date
    const sortedData = chartData.sort(
        (a, b) => new Date(a.name) - new Date(b.name)
    );

    const chart = useChart({
        data: sortedData,
        series: [{name: 'value', color: "teal.solid"}]
    })

    // console.log(chart.data)

    return(
        <>
        <Text>How many movies you logged each month</Text>
        <Chart.Root maxH="sm" chart={chart} >
            <LineChart data={chart.data} >
                <CartesianGrid stroke={chart.color("border")} vertical={false} />
                <XAxis 
                    axisLine={false}
                    dataKey={chart.key("name")}
                    stroke={chart.color("border")}
                    interval={0}
                    tick={{ angle: -45, textAnchor: "end" }}
                    />
                <YAxis 
                    axisLine={false}
                    tickLine={false}
                    tockMargin={10}
                    stroke={chart.color("border")}
                    />
                <Tooltip 
                    animationDuration={100}
                    cursor={false}
                    content={<Chart.Tooltip />}
                    />
                {chart.series.map((item) => (
                    <Line 
                    key={item.name}
                    isAnimationActive={false}
                    dataKey={chart.key(item.name)}
                    stroke={chart.color(item.color)}
                    strokeWidth={2}
                    dot={false}
                    />
                ))}
            </LineChart>
        </Chart.Root>
        </>
    )
};

export default YMLine;