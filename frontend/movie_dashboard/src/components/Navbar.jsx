import { Box, Flex, Heading, Link } from '@chakra-ui/react'

function Navbar(){
    return (
        <Box bg="bg.muted" px={6} py={5} color="white" position="fixed" top="0" left="0" width="100%" zIndex="1000">
            <Flex align="center" justify="space-between">
                <Heading size="xl"> Letterboxd Unboxed </Heading>

                <Flex gap={6}>
                    <Link href="#movies" _focus={{ outline: "none"}} _hover={{color:"white"}} color="blue.100" px={1.5} fontWeight="semibold" fontSize="lg" fontFamily="heading">Movies</Link>
                    <Link href="#stats" _focus={{ outline: "none"}} _hover={{color:"white"}} color="blue.100" px={1.5} fontWeight="semibold" fontSize="lg" fontFamily="heading">Stats</Link>
                    <Link href="#about" _focus={{ outline: "none"}} _hover={{color:"white"}} color="blue.100" px={1.5} fontWeight="semibold" fontSize="lg" fontFamily="heading">About</Link>
                </Flex>
            </Flex>
        </Box>
    )
}

export default Navbar;