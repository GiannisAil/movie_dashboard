import { Box } from "@chakra-ui/react"

function Stats({stats}){

    return(
        <Box>
            <h1>Letterboxd Movie Statistics</h1>
            <p>You have watched {stats.count} movies!</p>
            <p>On average each movie you watch is {stats.average_runtime} minutes long.</p>
        </Box>
    )
}

export default Stats;