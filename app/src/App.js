import './App.css';
import NussinovTable from './components/NussinovTable';

let handleFormSubmit = (event) => {
  event.preventDefault();
  console.log(event.target.sequence.value);
}

function App() {
  return (
    <div>
      <form onSubmit={handleFormSubmit}>
          <label>
            RNA Sequence: <input type="text" name="sequence" />
          </label>
          <button type="submit">Submit</button>
        </form>
      <NussinovTable />
    </div>
  );
}

export default App;
