import { useState } from 'react';
import Movie from '../components/Movie';
import UploadCSV from '../components/UploadCSV';
import Stats from '../components/Stats';
// import { getMovies } from '../services/api';
import Navbar from '../components/Navbar';
import { Box, Separator, Spinner } from '@chakra-ui/react'

function Home(){

    const [stats, setStats] = useState(null)

    return (
        <Box>
            <title>Letterboxd Unboxed</title>
            <UploadCSV statsChanger={setStats} />
            {stats && <Stats stats={stats} />}
        </Box>
    );
}

export default Home;