# Closest_Points

## Closest pair of points using Divide and Conquer

A graph containing randomly generated points is created.
This program uses divide and conquer to find the closest pair of points in the graph.

### Time Complexity: O(n.logn)

For further explanation to Ling Qi's video: <https://youtu.be/6u_hWxbOc7E>

Additionally, the program gives the correct result despite the sorting the 7 closest points' co-ordinates
by the x-coordinate only. Many tutorials suggest that the points also simultaneously be sorting by the y-coordinate.
I think this works because either way the points are greater than the distance 'd' which is (globally) the least distance between any two points on the graph.

Feel free to give feedback on this.

Thanks.
