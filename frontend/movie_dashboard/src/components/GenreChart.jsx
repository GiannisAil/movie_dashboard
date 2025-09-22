import { Chart, useChart } from "@chakra-ui/charts"
import { Text } from "@chakra-ui/react";
import { PieChart, Pie, Tooltip, Cell, Legend } from "recharts"

// TMDB genre IDs to genre names
const genreMap = { 28: "Action", 12: "Adventure", 16: "Animation", 35: "Comedy", 80: "Crime", 99: "Documentary", 
    18: "Drama", 10751: "Family", 14: "Fantasy", 36: "History", 27: "Horror", 10402: "Music", 
    9648: "Mystery", 10749: "Romance", 878: "Science Fiction", 10770: "TV Movie", 53: "Thriller", 
    10752: "War", 37: "Western" }

function GenreChart({stats}){
    const chartData = Object.entries(stats.favorite_genres).map(
        ([genreId, count]) => ({
            name: genreMap[genreId] || "Unknown",
            value: count,
        })
    );

    const chart = useChart({
        data: chartData,
        series: [{ name: 'value', color: "teal.solid"}]
    })

    console.log(chart.data)

    const COLORS = [
        "#0088FE", "#00C49F", "#FFBB28", "#FF8042", 
        "#A28DFF", "#FF6B8B", "#2ECC71", "#E67E22"
    ];

    return(
        <>
        <Text>Your most watched genres</Text>
        <Chart.Root maxH={"sm"} chart={chart} marginTop={1} scale={0.9}>
            <PieChart>
                <Pie
                    data={chart.data}
                    dataKey="value"
                    nameKey="name"
                    cx="50%"
                    cy="50%"
                    outerRadius={120}
                    fill="#8884d8"
                    label
                    >
                    {chart.data.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                </Pie>
                <Tooltip 
                    cursor={{ fill: chart.color("bg.muted") }}
                    animationDuration={100}
                    content={<Chart.Tooltip />}
                    />
                <Legend />
            </PieChart>
        </Chart.Root>
        </>
    )
}

export default GenreChart;