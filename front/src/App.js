import { BrowserRouter, Switch, Route, Routes } from "react-router-dom";

import NBALive from "./pages/nba_live";
import NBASchedule from "./pages/nba_schedule";
import NBAStandings from "./pages/nba_standings";
import Homepage from "./pages/homepage"

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Homepage />} />
        <Route path="/nba/live" element={<NBALive />} />
        <Route path="/nba/schedule" element={<NBASchedule />} />
        <Route path="/nba/standings" element={<NBAStandings />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;