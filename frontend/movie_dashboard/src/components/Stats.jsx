

function Stats({stats}){

    return(
        <div>
            <h4>Here come the stats!</h4>
            <p>You have watched {stats.count} movies!</p>
            <p>On average each movie you watch is {stats.average_runtime} minutes long.</p>
        </div>
    )
}

export default Stats;