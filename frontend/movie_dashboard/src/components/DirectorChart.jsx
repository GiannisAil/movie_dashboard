"use client"

import { Text } from "@chakra-ui/react";
import { Chart, useChart } from "@chakra-ui/charts"
import { Bar, BarChart, XAxis, YAxis, CartesianGrid, Tooltip } from "recharts"

function DirectorChart({stats}){
    // transform data to be ready to use in the chakra chart
    const chartData = Object.entries(stats.favorite_directors).map(
        ([director, count]) => ({
            director,
            count,
        })
    );

    const chart = useChart({
        data: chartData,
        series: [{ name: 'count', color: "teal.solid"}]
    })

    // console.log(chart.data)

    return(
        // <p>Your most watched director is: {stats.favorite_director}</p>
        <>
        <Text>Your most watched directors</Text>
        <Chart.Root maxH="sm" chart={chart}>
            <BarChart data={chart.data}>
                <CartesianGrid stroke={chart.color("border.muted")} vertical={false} />
                <XAxis 
                    axisLine={false} 
                    tickLine={false} 
                    dataKey={chart.key("director")}
                    interval={0}
                    tick={{ angle: -30, textAnchor: "end", fontSize: 12, dx: 25 }}    
                />
                <YAxis 
                    axisLine={false} 
                    tickLine={false} 
                    domain={[0,"auto"]} 
                />
                <Tooltip 
                    cursor={{ fill: chart.color("bg.muted") }}
                    animationDuration={100}
                    content={<Chart.Tooltip />}
                />
                {chart.series.map((item) => (
                    <Bar
                        key={item.name}
                        isAnimationActive={false}
                        dataKey={chart.key(item.name)}
                        fill={chart.color(item.color)}
                    />
                ))}
            </BarChart>
        </Chart.Root>
        </>
    )
}

export default DirectorChart;