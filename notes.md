## INTRODUCTION

  The Chess Project aims to develop a comprehensive chess engine and user
interface that allows users to play and analyze chess games. The project combines
elements of artificial intelligence, algorithm optimization, and user interface
design to create a robust and engaging chess experience. This system will be
capable of playing chess at various levels of difficulty, providing users with
feedback on their moves, and offering analysis tools for deeper understanding of
the game.

### **1. User Interface Module**
**objective**: *Create an interactive and intuitive graphical interface for the chess engine.*
   
  #### ➡Board display:
     
   - [x] Render a graphical representation of the chessboard.

      Create a `div` container for the chessboard.
      Define `div` elements for each square (8x8 grid).
      ``` html
      <div id="chessboard">
        <!-- Loop to create 64 squares -->
        <div class="square" id="a1"></div>
        <!-- More squares -->
      </div>
      ```
   - [ ] display pieces in their current positions.

      Represent pieces as unicode characters.
      > ♔ ♕ ♖ ♗ ♘ ♙	
      ``` javascript
      const initialPositions = {
        a1: '♖', a2: '♙', // etc.
      };
      
      function placePieces() {
        for (const [square, piece] of Object.entries(initialPositions)) {
          document.getElementById(square).innerHTML = `<img src="images/${piece}.png" alt="${piece}">`;
        }
      }
      document.addEventListener('DOMContentLoaded', placePieces);
      ```
  #### ➡Piece interaction:

   - [ ] Implement Drag and Drop functionality.
         Using native  API or library JQuery UI.

       ``` javascript
        document.querySelectorAll('.square img').forEach(img => {
          img.draggable = true;
          img.addEventListener('dragstart', onDragStart);
        });
        
        function onDragStart(event) {
          event.dataTransfer.setData('text/plain', event.target.id);
        }
        
        function onDrop(event) {
          event.preventDefault();
          const pieceId = event.dataTransfer.getData('text/plain');
          event.target.appendChild(document.getElementById(pieceId));
        }
        
        document.querySelectorAll('.square').forEach(square => {
          square.addEventListener('dragover', event => event.preventDefault());
          square.addEventListener('drop', onDrop);
        });
       ```


   
