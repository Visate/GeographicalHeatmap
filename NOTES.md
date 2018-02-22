## TODO:
- Initial code
- Read from CSV format
- Generate map (currently planned using matplotlib and the Basemap toolkit)
- Displaying areas around points
- Calculating distance between points

## NOTES TO SELF ABOUT THE MAP GENERATION
The imshow array is basically you need to do mapping for every single x,y pixel. 
So, all you have to do is create a huge array and just map all your points and the colours to it. 
The scaling can probably be done not extremely precisely, as much as 1 x/y value should be good enough due to how big the values are.
The eureka moment: https://matplotlib.org/gallery/images_contours_and_fields/image_demo.html#sphx-glr-gallery-images-contours-and-fields-image-demo-py

To figure out distance between the points, probably using pythagorean. A lot. And there's going to be a lot of number approximation.
Oh also probably a lot of using circles as well, but we'll see about that.
The gradiants should be tapering off near the middle of each other.

Seem to be unable to trust the map projection coordinates to give me anything useful, so I will just use the lat-lon and scale them appropriately.

What's with this weird rotation... 0,0 and max,max are correct positions, something wrong with the loop?
OKAY WHAT THE HECK X IS Y AND Y IS X WHAT IS LIFE ANYMORE
Okay so now that's out of the way, custom colour map... Tbh why am I doing this first
Should probably be doing the distance calculations
But it's a lot more complicated than it seems
Finding the distance between two points is easy enough, the issue is having awareness of all points
then determining whether that point should even have an effect on it at all.

In the minimap example, if I were to do this manually, I'd only be constrained by the bottom left point and the top right point
if I am to look from the top left point. 

Calculating the angle also between the two. That'll be a tough one.

Fortunately, because of the nature of using interpolation, I will be able to ignore the shading aspect and let it handle it for me.
The calculations for that would have been a nightmare.

I wonder if it will take for-looping through the entire thing to determine what colours the point should be?
Wait I was kidding maybe I do still have to set the values for interpolation manually :(((

## NUMBER CRUNCHING FOR MESH
Going to need some way to track the X axis and Y axis seperately, as well as the overall distance calculation as done using Pythagoras. 
Probably only need two of those variables, since I can just say positive = up and negative = down and vice versa for left and right.
If the distance is the least to just one of the points, then it will inherit the colour of just that one
If the distance is between two points and it is like right about the middle (probably have some variable to control the width of the gap) then set it to 0/white value
If it is close to more than one point, it takes the colour of whichever one is closer and reduces it by some kinda ratio...


## NOTES FROM JAN24
If the closest point is the same value then there shouldn't be any color dropoff
Possible colours: min: 10, max: 20

## QUESTIONS FOR FEB 20
- proposal for two different ideas to approach
a) Circular "power" influence
    - when doing the initial point clustering, intiially the point has a "strength value" of 1, which increases by 1 when it finds a new point within its radius, and adjusts the centre of the point accordingly.
    - two ways to approach overlap between circles: if the power of the overlapping circle is lower than the other one, either
        - reduce the shading on the primary circle in a similar fashion to how it already is based on a ratio between how much the power gap is between the two circles, but it could be completely be possible that the colour doesn't show up since it is just so isolated
        - make that circle visible and fade it out quicker based on how much weaker it is to
    - this makes the spacing between the points determinate, i.e. there could be lots of empty space on the map depending on how the radius is defined upon initialization
b) original but...
    - incorporate the "power weighting" system to the current map
    - goal is to make it look similar to other relevant heatmaps and I think this is the way to do it