def shapecast(
	bvh,
	intersectsBounds,
	intersectsRange,
	boundsTraverseOrder,
):
    offset = 0
    count = 8
    intersectsRange(offset, count)
