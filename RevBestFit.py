from dataclasses import dataclass, field
from typing import List, Tuple, Optional

@dataclass
class Rectangle:
    width: int
    height: int
    id: Optional[int] = None

@dataclass
class PackingResult:
    grid: List[List[int]]
    placements: List[Tuple[Rectangle, Tuple[int, int]]] = field(default_factory=list)
    total_waste: int = 0

class PackingProblem:
    def __init__(self, bin_width: int, bin_height: int):
        self.bin_width = bin_width
        self.bin_height = bin_height

    def pack_rectangles(self, rectangles: List[Rectangle]) -> PackingResult:
        sorted_rectangles = sorted(rectangles, key=lambda r: r.width * r.height, reverse=True)
        result = PackingResult(
            grid=[[0] * self.bin_width for _ in range(self.bin_height)]
        )
        for i, rect in enumerate(sorted_rectangles):
            rect.id = i + 1
            best_placement = None
            min_waste = float('inf')

            for y in range(self.bin_height - rect.height + 1):
                for x in range(self.bin_width - rect.width + 1):
                    if self._can_place(result.grid, x, y, rect):
                        waste = self._calculate_waste(result.grid, x, y, rect)
                        if waste < min_waste:
                            min_waste = waste
                            best_placement = (x, y, rect)

            if best_placement:
                x, y, final_rect = best_placement
                self._place_rectangle(result.grid, x, y, final_rect)
                result.placements.append((final_rect, (x, y)))
                result.total_waste = min_waste
            else:
                print(f"Could not place rectangle {rect.width}x{rect.height}")

        return result

    def _can_place(self, grid: List[List[int]], x: int, y: int, rect: Rectangle) -> bool:
        if x + rect.width > self.bin_width or y + rect.height > self.bin_height:
            return False

        return all(
            grid[y + i][x + j] == 0 
            for i in range(rect.height) 
            for j in range(rect.width)
        )

    def _place_rectangle(self, grid: List[List[int]], x: int, y: int, rect: Rectangle):
        for i in range(rect.height):
            for j in range(rect.width):
                grid[y + i][x + j] = rect.id

    def _calculate_waste(self, grid: List[List[int]], x: int, y: int, rect: Rectangle) -> int:
        temp_grid = [row[:] for row in grid]
        for i in range(rect.height):
            for j in range(rect.width):
                temp_grid[y + i][x + j] = rect.id

        return sum(row.count(0) for row in temp_grid)

    def visualize(self, result: PackingResult):
        print("Grid Layout:")
        for row in result.grid:
            print(" ".join(map(str, row)))
        
        print("\nRectangle Placements:")
        for rect, (x, y) in result.placements:
            print(f"Rectangle {rect.width}x{rect.height} (ID: {rect.id}) placed at ({x}, {y})")
        print(f"\nTotal Waste: {result.total_waste}")

def main():
    rectangles = [
        Rectangle(2, 4),
        Rectangle(6, 3),
        Rectangle(3, 2),
        Rectangle(4, 4),
        Rectangle(3, 6),
        Rectangle(4, 6)
    ]
    
    packing_problem = PackingProblem(bin_width=10, bin_height=10)
    result = packing_problem.pack_rectangles(rectangles)
    packing_problem.visualize(result)

if __name__ == "__main__":
    main()
