import { useState } from 'react';
import './App.css';
import Plot from 'react-plotly.js';

function App() {
  const [start, setStart] = useState('');
  const [end, setEnd] = useState('');
  const [fetching, setFetching] = useState(false);
  const [plotData, setPlotData] = useState([]);

  const generateTimeSeries = async () => {
    try {
      setFetching(true);
      const response = await fetch(`/generate_timeseries/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ start_date: start, end_date: end }),
      });
      const jsonData = await response.json();
      console.log(jsonData);
    } catch (error) {
      console.error('Error generating time series:', error);
    } finally {
      setFetching(false);
    }
  };

  const fetchData = async () => {
    try {
      const response = await fetch(`/fetch_timeseries/?start_date=${start}&end_date=${end}`);
      const jsonData = await response.json();

      const plotDates = jsonData.map(entry => entry.timestamp);
      const plotSolarPower = jsonData.map(entry => entry.solar_power);

      setPlotData([
        {
          x: plotDates,
          y: plotSolarPower,
          type: 'scatter',
          mode: 'lines+markers',
          marker: { color: 'blue' },
          name: 'Solar Power',
        }
      ]);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  return (
    <div className="App">
      <h1>Solar Power Time Series Generator and Plotter</h1>
      <div>
        <input
          type="text"
          placeholder="Start Date (YYYY-MM-DD)"
          value={start}
          onChange={(e) => setStart(e.target.value)}
        />
        <input
          type="text"
          placeholder="End Date (YYYY-MM-DD)"
          value={end}
          onChange={(e) => setEnd(e.target.value)}
        />
        <button onClick={generateTimeSeries} disabled={fetching}>
          {fetching ? 'Generating...' : 'Generate Time Series'}
        </button>
        <button onClick={fetchData}>Fetch and Plot Time Series</button>
      </div>
      {plotData.length > 0 && (
        <div>
          <h2>Solar Power Time Series</h2>
          <Plot
            data={plotData}
            layout={{ title: 'Solar Power Time Series', xaxis: { title: 'Timestamp' }, yaxis: { title: 'Solar Power' } }}
          />
        </div>
      )}
    </div>
  );
}

export default App;
