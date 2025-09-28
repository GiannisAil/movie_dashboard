import { Text, Box, List } from "@chakra-ui/react";

function GeneralList({stats}){
    return(
        <Box paddingBottom={10} borderRadius={"md"} border="1px solid" p="6" m="4" w="fit-content" mx="auto">
            <Text fontSize="xl" mb={4} fontWeight="bold">General Stats</Text>
            <List.Root as="ul" pl="0" textAlign={"left"} mx="auto" maxW="fit-content">
                <List.Item>
                    Movies Logged: {stats.count}
                </List.Item>
                <List.Item>
                    Average Release Year: {stats.average_year}
                </List.Item>
                <List.Item>
                    Average Runtime: {stats.average_runtime}
                </List.Item>
                <List.Item>
                    Oldest Movie Logged: {stats.oldest_movie.name} - {stats.oldest_movie.year}
                </List.Item>
                <List.Item>
                    Newest Movie Logged: {stats.newest_movie.name} - {stats.newest_movie.year}
                </List.Item>
                <List.Item>
                    Longest Movie Logged: {stats.longest_movie.name} which is {stats.longest_movie.runtime} minutes long.
                </List.Item>
            </List.Root>
        </Box>
    )
}

export default GeneralList