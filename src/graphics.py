def computePixelSize(gridWidth,gridHeight,bigSide):
	if gridWidth > gridHeight:
		factor = gridWidth/gridHeight
		width = bigSide
		height = int(bigSide/factor)
		pixelSize = width/gridWidth

	elif gridWidth < gridHeight:
		factor = gridHeight/gridWidth
		height = bigSide
		width = int(bigSide/factor)
		pixelSize = height/gridHeight
		
	else:
		factor = 1
		width = bigSide
		height = bigSide
		pixelSize = bigSide/gridWidth

	return pixelSize,width,height