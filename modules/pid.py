def calculate(x,targetX,y,targetY,P,D,lastdeltaX,lastdeltaY,minError):
    errorX = targetX-x
    errorY = targetY-y
    if errorX < minError:
        errorX = 0
    if errorY < minError:
        errorY = 0
    correctX = P*errorX + D*(errorX-lastdeltaX)
    correctY = P*errorY + D*(errorY-lastdeltaY)
    return [correctX,correctY,errorX,errorY]
