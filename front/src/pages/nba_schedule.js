import Datepicker from "tailwind-datepicker-react"
import React, { useState, useEffect } from 'react';

import Header from '../components/Header'


export default function NBAMatches() {
  const options = {
    title: "Pick date",
    autoHide: true
  }

  const [show, setShow] = useState([])
  const url = 'http://localhost:8000/nba/schedule/'
  const [games, setGames] = useState([])
  const [date, setDate] = useState(new Date())

  const handleChange = (selectedDate) => {
    setDate(selectedDate)
  }

  useEffect(() => {
    fetch(url + date.toLocaleDateString().replaceAll(".", ""))
      .then((res) => res.json())
      .then((d) => setGames(d))
  }, [date]);

  const handleClose = (state) => {
    setShow(state)
  }

  return (
    <>
      <Header />
      <main className="grid place-items-center bg-white px-6 py-4 sm:py-24 lg:px-8 space-y-10">
        <div class="w-60">
          <Datepicker options={options} onChange={handleChange} show={show} setShow={handleClose} />
        </div>
        <div className="text-center">
          <div>
            {games.map((game, index) => {
              return (
                <div class={`border-gray-200 ${game.gameStatus === 2 ? ("border-red-500 border-b-2") : ("border-gray-200 border-b")} hover:border-blue-700 hover:border-b-2 hover:bg-neutral-50`}>
                  <div class="grid grid-cols-5 gap-10 place-items-center h-40">
                    <div class="py-4">
                      <span class="leading-7 text-gray-800 text-lg">{game.homeTeam.team}</span>
                    </div>
                    <div>
                      <img class="h-20 py-2 pr-4 ml-8" src={`https://cdn.nba.com/logos/nba/${game.homeTeam.teamId}/global/L/logo.svg`} alt="" />
                    </div>
                    <div>
                      <span className={`mt-4 text-3xl font-semibold font-sans tracking-tight ${game.gameStatus === 2 ? ("text-red-500") : ("text-gray-900")} sm:text-2xl`}>{game.gameStatus !== 1 ? (game.homeTeam.score + " : " + game.awayTeam.score) : ("TBD")}</span>
                      <br></br>
                      <span class="leading-7 text-gray-600 text-xs">{game.gameStatusText}</span>
                    </div>
                    <div>
                      <img class="h-20 py-2 pr-4 ml-8" src={`https://cdn.nba.com/logos/nba/${game.awayTeam.teamId}/global/L/logo.svg`} alt="" />
                    </div>
                    <div>
                      <span class="leading-7 text-gray-800 text-lg">{game.awayTeam.team}</span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </main>
    </>
  )
}