import React, { useState, useEffect } from 'react';

import Header from '../components/Header'

export default function NBAMatches() {
    const url = 'http://localhost:8001/nba/standings'
    const [standings, setStandings] = useState([])


    const fetchInfo = () => {
        return fetch(url)
            .then((res) => res.json())
            .then((d) => setStandings(d))
    }

    useEffect(() => {
        fetchInfo();
    }, []);

    return (
        <>
            <Header />
            <main className="grid place-items-center bg-white px-6 py-4 sm:py-20 lg:px-8">
                <div className="text-center">
                    <div class="bg-slate-100 font-semibold">
                        <div class="grid grid-cols-7 gap-1 place-items-center h-35">
                            <div class="py-4">
                                <span class="leading-7 text-gray-800 text-m">Place</span>
                            </div>
                            <div>
                            </div>
                            <div>
                                <span class="leading-7 text-gray-600 text-m">Team</span>
                            </div>
                            <div>
                                <span class="leading-7 text-gray-600 text-m">W</span>
                            </div>
                            <div>
                                <span class="leading-7 text-gray-600 text-m">L</span>
                            </div>
                            <div>
                                <span class="leading-7 text-gray-600 text-m">Last 10</span>
                            </div>
                            <div>
                                <span class="leading-7 text-gray-600 text-m">Conference</span>
                            </div>
                        </div>
                    </div>
                    {standings.map((standing, index) => {
                        return (
                            <div class="border-b border-gray-200 hover:border-blue-700 hover:border-b-2 hover:bg-neutral-50">
                                <div class="grid grid-cols-7 gap-1 place-items-center h-30">
                                    <div class="py-4">
                                        <span class="leading-7 text-gray-800 text-m">{index + 1}</span>
                                    </div>
                                    <div>
                                        <img class="h-20 py-2 pr-4 ml-8" src={`https://cdn.nba.com/logos/nba/${standing.teamId}/global/L/logo.svg`} alt="" />
                                    </div>
                                    <div>
                                        <span class="leading-7 text-gray-600 text-m">{standing.team}</span>
                                    </div>
                                    <div>
                                        <span class="leading-7 text-gray-600 text-m">{standing.wins}</span>
                                    </div>
                                    <div>
                                        <span class="leading-7 text-gray-600 text-m">{standing.losses}</span>
                                    </div>
                                    <div>
                                        <span class="leading-7 text-gray-600 text-m">{standing.last_10}</span>
                                    </div>
                                    <div>
                                        <span class="leading-7 text-gray-600 text-m">{standing.conference}</span>
                                    </div>
                                </div>
                            </div>
                        );
                    })}
                </div>
            </main >
        </>
    )
}