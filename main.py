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

import webapp2
from sudokusolver import ValidationException, SudokuSolver

class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')
        
class Solve(webapp2.RequestHandler):
    
    def get(self, puzzle_line):
        self.response.headers['Content-Type'] = 'text/plain'
        solver = SudokuSolver()
        try:
            puzzle_grid = solver.build_grid(puzzle_line)
            solved = solver.solve(puzzle_grid)
            self.response.write(solved)
        except ValidationException as e:
            self.response.status_int = 400
            self.response.write(e.value)
        
class Hint(webapp2.RequestHandler):
    
    def get(self, puzzle_line):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.status_int = 501
        self.response.write('Not yet implemented')


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/solve/(\d+)', Solve),
    ('/hint/(\d+)', Hint)
], debug=True)