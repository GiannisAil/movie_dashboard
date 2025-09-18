import { Box, Heading, Text } from "@chakra-ui/react"
import DirectorChart from "./DirectorChart";

function Stats({stats}){

    return(
        <Box>
            <Heading size="3xl" paddingBottom="3">Your Letterboxd Movie Statistics</Heading>
            <Text>You have watched {stats.count} movies!</Text>
            <Text>On average each movie you watch is {stats.average_runtime} minutes long.</Text>
            <DirectorChart stats={stats} />
        </Box>
    )
}

export default Stats;