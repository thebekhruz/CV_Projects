import java.util.*;

public class MoveChooser {

  static BoardState result(BoardState boardState, Move move) {
    BoardState boardState1 = boardState.deepCopy();
    boardState1.makeLegalMove(move.x, move.y);
    return boardState1;
  }

  static int evaluate(BoardState board, int colour) {
    int[][] points = {
        { 120, -20, 20, 5, 5, 20, -20, 120 },
        { -20, -40, -5, -5, -5, -5, -40, -20 },
        { 20, -5, 15, 3, 3, 15, -5, 20 },
        { 5, -5, 3, 3, 3, 3, -5, 5 },
        { 5, -5, 3, 3, 3, 3, -5, 5 },
        { 20, -5, 15, 3, 3, 15, -5, 20 },
        { -20, -40, -5, -5, -5, -5, -40, -20 },
        { 120, -20, 20, 5, 5, 20, -20, 120 },
    };

    int boardValue = 0;
    int blackValue = 0;
    int whiteValue = 0;
    for (int i = 0; i < 8; i++) {
      for (int j = 0; j < 8; j++) {
        if (board.getContents(i, j) == -1) {
          blackValue += points[i][j] * board.getContents(i, j);

        } else {
          whiteValue += points[i][j] * board.getContents(i, j);

        }
      }
      boardValue = whiteValue - blackValue;
    }
    return boardValue;
  }

  static int minimaxVal(BoardState boardState, int depth, int alpha, int beta) {
    int color = boardState.colour;
    ArrayList<Move> moves = boardState.getLegalMoves(); // returns first 2

    if (depth == 0 || boardState.gameOver() == true) {
      return evaluate(boardState, boardState.colour); // returns boardvalue
    }

    // Maximizing node
    else if (color == -1) {
      int maxEval = -1000000;
      for (Move i : moves) {
        color = boardState.colour * -1;
        maxEval = Math.max(maxEval, minimaxVal(result(boardState, i), depth - 1, alpha, beta));
        if (maxEval >= beta) {
          return maxEval;
        }
        alpha = Math.max(alpha, maxEval);
      }
      return maxEval;
    }
    // blacks turn
    else {
      int minEval = 1000000;
      for (Move i : boardState.getLegalMoves()) {
        // boardState.colour = 1;
        minEval = Math.min(minEval, minimaxVal(result(boardState, i), depth - 1, alpha, beta));
        if (minEval <= alpha) {
          return minEval;
        }
        beta = Math.min(beta, minEval);
      }
      return minEval;
    }
  }

  static Move minimax(BoardState boardState, int depth, int alpha, int beta) {

    ArrayList<Move> availableMoves = boardState.getLegalMoves();

    int value = minimaxVal(boardState, depth, alpha, beta);

    // System.out.println(value);
    // System.out.println("waaa");

    for (Move m : availableMoves) {
      int x = minimaxVal(result(boardState, m), depth - 1, alpha, beta);
      if (value == x) {
        return m;
      }
    }
    System.out.println("waaa");
    return availableMoves.get(0);

  }

  public static Move chooseMove(BoardState boardState) {

    int searchDepth = Othello.searchDepth;
    ArrayList<Move> moves = boardState.getLegalMoves();

    if (moves.isEmpty()) {
      return null;
    }

    return minimax(boardState, searchDepth, -1000000, 1000000);

  }
}
