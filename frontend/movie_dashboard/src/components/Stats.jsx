import { Box, Heading, Text, Flex} from "@chakra-ui/react"
import DirectorChart from "./DirectorChart";
import GenreChart from "./GenreChart";
import YMLine from "./YMLine";

function Stats({stats}){

    return(
        <Box>
            <Heading size="3xl" paddingBottom="3">Your Letterboxd Movie Statistics</Heading>
            {/* <Text>You have watched {stats.count} movies!</Text>
            <Text>On average each movie you watch is {stats.average_runtime} minutes long.</Text> */}
            <Flex gap={8}>
                <Box flex={1} w="400px">
                    <DirectorChart stats={stats} />
                </Box>
                <Box flex={1} w="400px">
                    <GenreChart stats={stats} />
                </Box>
                <Box flex={1} w="400px">
                    <YMLine stats={stats} />
                </Box>
            </Flex>
        </Box>
    )
}

export default Stats;