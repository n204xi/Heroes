import React from "react";

const CHARACTERS = [
  "Moritz",
  "Vanitas",
  "Sora",
  "Connor",
  "Baymax",
  "Tadashi"
];

function CharacterSelect({ character, setCharacter }) {
  return (
    <div style={{ marginBottom: 10 }}>
      <label>
        <b>Choose Character: </b>
        <select value={character} onChange={e => setCharacter(e.target.value)}>
          {CHARACTERS.map(c => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>
      </label>
    </div>
  );
}

export default CharacterSelect;