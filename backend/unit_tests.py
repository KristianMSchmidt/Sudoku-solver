import unittest
from sudoku_algorithm import *

do_slow_test = True

class Tests(unittest.TestCase):
    def test_tiles(self):
        """
        Testing the TILES-constant
        """
        EXPEC = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 
                 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 
                 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 
                 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9',
                 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 
                 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9',
                 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9',
                 'I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9']
        self.assertEqual(TILES, EXPEC)
    
    def test_all_constraints(self):
        """
        Testing the ALL_CONSTRAINTS set generated by the gen_constraints function
        """
        #  row constraints
        self.assertTrue(('A1', 'A7') in ALL_CONSTRAINTS )
        self.assertTrue(('A7', 'A1') in ALL_CONSTRAINTS )
        self.assertTrue(('I2', 'I7') in ALL_CONSTRAINTS )
        self.assertTrue(('I7', 'I2') in ALL_CONSTRAINTS )
        
        #column constraints
        self.assertTrue(('A1', 'I1') in ALL_CONSTRAINTS )
        self.assertTrue(('I1', 'A1') in ALL_CONSTRAINTS )
        self.assertTrue(('C3', 'H3') in ALL_CONSTRAINTS )
        self.assertTrue(('H3', 'C3') in ALL_CONSTRAINTS )

        #square constraints
        self.assertTrue(('A1', 'C3') in ALL_CONSTRAINTS )
        self.assertTrue(('C3', 'A1') in ALL_CONSTRAINTS )
        self.assertTrue(('D6', 'F4') in ALL_CONSTRAINTS )
        self.assertTrue(('F4', 'D6') in ALL_CONSTRAINTS )
        self.assertTrue(('A9', 'B7') in ALL_CONSTRAINTS )
        self.assertTrue(('B7', 'A9') in ALL_CONSTRAINTS )
        
        # check that not all pairs are in the constraint set
        self.assertFalse(('A1', 'B4') in ALL_CONSTRAINTS)
        self.assertFalse(('B2', 'C7') in ALL_CONSTRAINTS)
        self.assertFalse(('I5', 'H8') in ALL_CONSTRAINTS)
        self.assertFalse(('A1', 'A1') in ALL_CONSTRAINTS)
        self.assertFalse(('I5', 'I5') in ALL_CONSTRAINTS)
        
        # in total, there should be 81*20 = 1620 constraints in the set. Let's check this
        self.assertEqual(len(ALL_CONSTRAINTS), 1620)

    def test_constraint_dict(self):
        """
        Testing the CONSTRAINT_DICT dictionary generated by the gen_constraints function
        """
        #  lets just test the (key,value)-pair, where the key is 'A1'
        expected = set()
        row_constraints = [('A2', 'A1'),('A3', 'A1'),('A4', 'A1'),('A5', 'A1'),('A6', 'A1'),('A7', 'A1'),('A8', 'A1'),('A9', 'A1')]
        column_constraints = [('B1', 'A1'),('C1', 'A1'),('D1', 'A1'),('E1', 'A1'),('F1', 'A1'),('G1', 'A1'),('H1', 'A1'),('I1', 'A1')]
        square_constraints = [('B2', 'A1'),('B3', 'A1'),('C2', 'A1'),('C3', 'A1')]
        expected.update(row_constraints)
        expected.update(column_constraints)
        expected.update(square_constraints)
        self.assertEqual(expected, CONSTRAINT_DICT['A1'])
        # All values in the dict should have the length 8 + 8 + 4 = 20. So let's check this:
        for key, val in CONSTRAINT_DICT.items():
            self.assertEqual(len(val), 20)

    def test_gen_board(self):
        sudoku_string = "000260701680070090190004500820100040004602900050003028009300074040050036703018000"
        sudoku = gen_board(sudoku_string)
        self.assertEqual(sudoku['A1'], set([1,2,3,4,5,6,7,8,9]))
        self.assertEqual(sudoku['I9'], set([1,2,3,4,5,6,7,8,9]))
        self.assertEqual(sudoku['A4'], set([2]))
        self.assertEqual(sudoku['A5'], set([6]))
    
    def test_issolved(self):
        """
        Testing the is_solved function and all unsolved and solved sudokus in our library
        """
        with open("sudokus_start.txt") as file:
            all_sudokus = [line.strip() for line in file]
        for sudoku in all_sudokus:
            self.assertFalse(is_solved(gen_board(sudoku)))

        with open("sudokus_finish.txt") as file:
            all_solutions = [line.strip() for line in file]
        for solution in all_solutions:
            self.assertTrue(is_solved(gen_board(solution.split(" ")[0])))
       
      
    def test_AC_3_all_constraints(self):
        """ 
        This function is not yet properly tested. I only test that it finds
        some obvious arc-consistencies and returns false in these cases. 
        """
        #AC_3 should return an arc-reduced sudoku, is no inconsistancies are found (non-false)
        solvable_sudoku = "000008900603049010000500600004000009230000001050002060007000000302051000508960203"
        self.assertTrue(AC_3_all_constraints(gen_board(solvable_sudoku)))

        #AC_3 should return false an inconsistancy is found (sudoku in not solvable)    
        
        # break of row constraint    
        unsolvable_sudoku = "110008900603049010000500600004000009230000001050002060007000000302051000508960203"
        self.assertFalse(AC_3_all_constraints(gen_board(unsolvable_sudoku)))

        #break of column constraint
        unsolvable_sudoku = "200008900623049010000500600004000009230000001050002060007000000302051000508960203"
        self.assertFalse(AC_3_all_constraints(gen_board(unsolvable_sudoku)))
        
        # break of square constraint
        unsolvable_sudoku = "200008900203049010000500600004000009230000001050002060007000000302051000508960203"
        self.assertFalse(AC_3_all_constraints(gen_board(unsolvable_sudoku)))
  
    
    if do_slow_test:        
        def test_sudoku_solver(self):
            """
            Test sudoku solved by solving all 400 sudokus in the library and comparing with the known solutions
            """
            with open("sudokus_finish.txt") as file:
                all_solutions = [line.strip() for line in file]

            with open("sudokus_start.txt") as all_sudokus:
                for i, sudoku in enumerate(all_sudokus):
                    calculated = sudoku_solver(sudoku)
                    expected = all_solutions[i]
                    self.assertEqual(calculated,  expected)
             
if __name__ == '__main__':
    unittest.main()
