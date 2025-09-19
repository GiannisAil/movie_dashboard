import { Box, Heading, Text } from "@chakra-ui/react"
import DirectorChart from "./DirectorChart";
import GenreChart from "./GenreChart";
import YMLine from "./YMLine";

function Stats({stats}){

    return(
        <Box>
            <Heading size="3xl" paddingBottom="3">Your Letterboxd Movie Statistics</Heading>
            <Text>You have watched {stats.count} movies!</Text>
            <Text>On average each movie you watch is {stats.average_runtime} minutes long.</Text>
            <DirectorChart stats={stats} />
            <GenreChart stats={stats} />
            <YMLine stats={stats} />
        </Box>
    )
}

export default Stats;