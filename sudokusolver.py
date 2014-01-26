'''
Created on 27/01/2014

@author: Adam Speakman

@contact: https://github.com/adamsp

@license: Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import re

class ValidationException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
class SudokuSolver:
    
    def __init__(self):
        self.MAX_ITERATIONS = 81;
        self.invalid_line_pattern = re.compile("[^0-9]")

    def unique(self, values):
        unique_values = ''.join(set(values))
        # We allow any number of 0's as placeholders, so we check that the unique length without 0's
        # is the same as the original length without 0's - if it is, then original input is unique :)
        return (len(unique_values) - unique_values.count('0')) == (len(values) - values.count('0'))
    
    def col(self, puzzle_grid, index):
        column = ''
        for col in puzzle_grid:
            column += col[index]
        return column
    
    def row(self, puzzle_grid, index):
        return puzzle_grid[index]
    
    def top_left(self, puzzle_grid):
        return puzzle_grid[0][:3] + puzzle_grid[1][:3] + puzzle_grid[2][:3]
    
    def top_mid(self, puzzle_grid):
        return puzzle_grid[0][3:6] + puzzle_grid[1][3:6] + puzzle_grid[2][3:6]    
        
    def top_right(self, puzzle_grid):
        return puzzle_grid[0][6:] + puzzle_grid[1][6:] + puzzle_grid[2][6:]
        
    def cen_left(self, puzzle_grid):
        return puzzle_grid[3][:3] + puzzle_grid[4][:3] + puzzle_grid[5][:3]
        
    def cen_mid(self, puzzle_grid):
        return puzzle_grid[3][3:6] + puzzle_grid[4][3:6] + puzzle_grid[5][3:6]
        
    def cen_right(self, puzzle_grid):
        return puzzle_grid[3][6:] + puzzle_grid[4][6:] + puzzle_grid[5][6:]
        
    def bot_left(self, puzzle_grid):
        return puzzle_grid[6][:3] + puzzle_grid[7][:3] + puzzle_grid[8][:3]
        
    def bot_mid(self, puzzle_grid):
        return puzzle_grid[6][3:6] + puzzle_grid[7][3:6] + puzzle_grid[8][3:6]
        
    def bot_right(self, puzzle_grid):
        return puzzle_grid[6][6:] + puzzle_grid[7][6:] + puzzle_grid[8][6:]
            
    def finished(self, puzzle_grid):
        for line in puzzle_grid:
            if line.count('0') > 0:
                return False
        return True
    
    def missing_entries(self, values):
        missing = ''
        if values.count('1') == 0:
            missing += '1'
        if values.count('2') == 0:
            missing += '2'
        if values.count('3') == 0:
            missing += '3'
        if values.count('4') == 0:
            missing += '4'
        if values.count('5') == 0:
            missing += '5'
        if values.count('6') == 0:
            missing += '6'
        if values.count('7') == 0:
            missing += '7'
        if values.count('8') == 0:
            missing += '8'
        if values.count('9') == 0:
            missing += '9'
        return missing        
    
    # Merges potential values for a cell from its row, column and grid potentials, into a single set.
    # A potential must exist in all 3 for it to be valid - if it doesn't exist in one, then it can't exist in this cell.
    def merge_potentials(self, vals_1, vals_2, vals_3):
        results = ''
        for val in vals_1:
            if vals_2.count(val) == 1 and vals_3.count(val) == 1:
                results += val
        return results
    
    def validate_puzzle_grid(self, puzzle_grid):
        for col_index in range(0,9):
            column = self.col(puzzle_grid, col_index)
            if not self.unique(column):
                raise ValidationException('Invalid column - no duplicate entries allowed, except 0 as placeholder.')
        if not self.unique(self.top_left(puzzle_grid)):
            raise ValidationException('Your top left 3x3 has duplicate entries.')
        elif not self.unique(self.top_mid(puzzle_grid)):
            raise ValidationException('Your top middle 3x3 has duplicate entries.')
        elif not self.unique(self.top_right(puzzle_grid)):
            raise ValidationException('Your top right 3x3 has duplicate entries.')
        elif not self.unique(self.cen_left(puzzle_grid)):
            raise ValidationException('Your center left 3x3 has duplicate entries.')
        elif not self.unique(self.cen_mid(puzzle_grid)):
            raise ValidationException('Your center middle 3x3 has duplicate entries.')
        elif not self.unique(self.cen_right(puzzle_grid)):
            raise ValidationException('Your center right 3x3 has duplicate entries.')
        elif not self.unique(self.bot_left(puzzle_grid)):
            raise ValidationException('Your bottom left 3x3 has duplicate entries.')
        elif not self.unique(self.bot_mid(puzzle_grid)):
            raise ValidationException('Your bottom middle 3x3 has duplicate entries.')
        elif not self.unique(self.bot_right(puzzle_grid)):
            raise ValidationException('Your bottom right 3x3 has duplicate entries.')
    
    def build_grid(self, puzze_line):
        if len(puzze_line) != 81:
            raise ValidationException('Invalid input - must be exactly 81 digits long')
        elif self.invalid_line_pattern.match(puzze_line):
            raise ValidationException('Invalid input - numbers 0 through 9 only.')
        count = 0
        puzzle_grid = []
        while count < 81:
            current_row = puzze_line[count:count+9]
            if not self.unique(current_row):
                raise ValidationException('Invalid input - no duplicate entries allowed for a row, except 0 as placeholder.')
            # Have to make an array out of the string here, cos we can't directly update an index later if we don't.
            puzzle_row = []
            for i in current_row:
                puzzle_row.append(i)
            puzzle_grid.append(puzzle_row)
            count += 9
        self.validate_puzzle_grid(puzzle_grid)
        return puzzle_grid
    
    # Assumes valid input
    def solve(self, puzzle_grid):
        iterations = 0
        while iterations < self.MAX_ITERATIONS and not self.finished(puzzle_grid):
            iterations += 1
            # Build a collection of missing elements for each row, column and 3x3 'grid'
            row_potentials = []
            for row_index in range(0,9):
                # These are the missing entries for this row
                row_potentials.append(self.missing_entries(self.row(puzzle_grid, row_index)))
            col_potentials = []
            for col_index in range(0,9):
                # These are the missing entries for this column
                col_potentials.append(self.missing_entries(self.col(puzzle_grid, col_index)))
            grid_potentials = []
            # These are the missing entries for each 3x3 grid
            grid_potentials.append(self.missing_entries(self.top_left(puzzle_grid)))
            grid_potentials.append(self.missing_entries(self.top_mid(puzzle_grid)))
            grid_potentials.append(self.missing_entries(self.top_right(puzzle_grid)))
            grid_potentials.append(self.missing_entries(self.cen_left(puzzle_grid)))
            grid_potentials.append(self.missing_entries(self.cen_mid(puzzle_grid)))
            grid_potentials.append(self.missing_entries(self.cen_right(puzzle_grid)))
            grid_potentials.append(self.missing_entries(self.bot_left(puzzle_grid)))
            grid_potentials.append(self.missing_entries(self.bot_mid(puzzle_grid)))
            grid_potentials.append(self.missing_entries(self.bot_right(puzzle_grid)))
            
            # Each cell has a set of 'potential' entries for its row, and for its column, and for its grid.
            # Must remove any that don't match.
            # For example if an element matched 1,4,5 in its row, 1,4,6 in its column and 1,3,5 in its grid,
            # then it has to be 1 - since 3,4,5,6 are all cancelled out (each of those already exists in some
            # other area)
            potentials_grid = []
            for row_index in range(0,9):
                row_individual_potentials = []
                for col_index in range(0,9):
                    cell_potentials = ''
                    if puzzle_grid[row_index][col_index] != '0':
                        # This cell has already been populated. This is the only potential entry in this cell.
                        cell_potentials = puzzle_grid[row_index][col_index]
                    else:
                        grid_index = (col_index / 3) + 3 * (row_index / 3)
                        cell_potentials = self.merge_potentials(row_potentials[row_index], col_potentials[col_index], grid_potentials[grid_index])
                    row_individual_potentials.append(cell_potentials)
                potentials_grid.append(row_individual_potentials)
                
            # Now we have our set of potential entries for each cell. Can we cancel out any more? Sure!
            # If a cell is the only cell in its row, column, or grid which contains a given potential element,
            # then that element must be the entry for that cell.
            # For example if a cell contains potentials [3,5,7] and no other cell in its row, column or grid
            # contains 3 in its potentials, then this cells entry must be the value 3.
            for row_index in range(0,9):
                for col_index in range(0,9):
                    if len(potentials_grid[row_index][col_index]) == 1:
                        # This cell only has 1 possible entry.
                        continue
                    for potential in potentials_grid[row_index][col_index]:
                        potential_found = False
                        # Check other entries in row
                        row_potentials = self.row(potentials_grid, row_index)
                        for other_potential in row_potentials[:col_index]:
                            # Entries before the current column
                            if other_potential == potential:
                                potential_found = True
                                break
                        if potential_found: # No point checking for more - there's > 1 possible places for this entry.
                            break
                        for other_potential in row_potentials[col_index:]:
                            # Entries after the current column
                            if other_potential == potential:
                                potential_found = True
                                break
                        if potential_found: # No point checking for more - there's > 1 possible places for this entry.
                            break
                        
                        # Check other entries in column
                        col_potentials = self.col(potentials_grid, col_index)
                        for other_potential in col_potentials[:row_index]:
                            # Entries before the current row
                            if other_potential == potential:
                                potential_found = True
                                break
                        if potential_found: # No point checking for more - there's > 1 possible places for this entry.
                            break
                        for other_potential in col_potentials[row_index:]:
                            # Entries after the current row
                            if other_potential == potential:
                                potential_found = True
                                break
                        if potential_found: # No point checking for more - there's > 1 possible places for this entry.
                            break
                        
                        # Check other entries in 3x3 grid
                        grid_index = (col_index % 3) + 3 * (row_index % 3)
                        grid_potentials = []
                        if grid_index == 0:
                            grid_potentials = self.top_left(potentials_grid)
                        elif grid_index == 1:
                            grid_potentials = self.top_mid(potentials_grid)
                        elif grid_index == 2:
                            grid_potentials = self.top_right(potentials_grid)
                        elif grid_index == 3:
                            grid_potentials = self.cen_left(potentials_grid)
                        elif grid_index == 4:
                            grid_potentials = self.cen_mid(potentials_grid)
                        elif grid_index == 5:
                            grid_potentials = self.cen_right(potentials_grid)
                        elif grid_index == 6:
                            grid_potentials = self.bot_left(potentials_grid)
                        elif grid_index == 7:
                            grid_potentials = self.bot_mid(potentials_grid)
                        else: # grid_index == 8:
                            grid_potentials = self.bot_right(potentials_grid)
                        
                        current_grid_index = (col_index % 3) + 3 * (row_index % 3)
                        for other_potential in grid_potentials[:current_grid_index]:
                            # Entries before the current column
                            if other_potential == potential:
                                potential_found = True
                                break
                        if potential_found: # No point checking for more - there's > 1 possible places for this entry.
                            break
                        for other_potential in grid_potentials[current_grid_index:]:
                            # Entries after the current column
                            if other_potential == potential:
                                potential_found = True
                                break
                        if potential_found: # No point checking for more - there's > 1 possible places for this entry.
                            break
                        
                        # We have not found this potential in any other set of potentials for other elements in its
                        # row, column or grid. This is the one!
                        potentials_grid[row_index][col_index] = potential
                        
            # Finally, we go through our potentials grid and find every potentials list of length 1. This is the entry
            # for that cell, so we put it into our input grid and then go through again until we've found them all.
            for row_index in range(0,9):
                for col_index in range(0,9):
                    if len(potentials_grid[row_index][col_index]) == 1:
                        puzzle_grid[row_index][col_index] = str(potentials_grid[row_index][col_index])
                        
        # Ok we have a solution!
        solved = ''
        for row_index in range(0,9):
            solved += ''.join(puzzle_grid[row_index])
        return solved

