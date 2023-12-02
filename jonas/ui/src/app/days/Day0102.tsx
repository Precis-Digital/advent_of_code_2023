"use client"
import { Divider, Grid, Typography } from "@mui/material"
import React, { ReactElement, useEffect } from "react"
import { drawText } from "./Day0101"
import { useSearchParams } from "next/navigation"

const Day0102 = (): ReactElement => {
    const day1TaskCanvasRef = React.useRef<HTMLCanvasElement>(null)
    const [day1Task2, setDay1Task2] = React.useState<string[] | undefined>(undefined)
    const day1TaskSampleCanvasRef = React.useRef<HTMLCanvasElement>(null)
    const [day1Task2Sample, setDay1Task2Sample] = React.useState<string[] | undefined>(undefined)
    const [fps, setFps] = React.useState<number>(10)

    const searchParams = useSearchParams()

    useEffect(() => {
        if (searchParams.get('fps') != null) {
            setFps(parseInt(searchParams.get('fps') as string))
        }
    }, [searchParams])

    useEffect(() => {
        fetch('/api/files/Day01_1').then((resp) => {
            resp.json().then(data => {
                setDay1Task2(data.data.split('\n'))
            })
        })

        fetch('/api/files/Day01_2_sample').then((resp) => {
            resp.json().then(data => {
                setDay1Task2Sample(data.data.split('\n'))
            })
        })
    }, [])

    useEffect(() => {
        if (day1TaskSampleCanvasRef.current == null) return
        if (day1Task2Sample == null) return
        const canvas = day1TaskSampleCanvasRef.current
        const context = canvas.getContext('2d')
        if (context == null) return

        drawTask2Starter(context, day1Task2Sample, fps)

    }, [day1Task2Sample])

    useEffect(() => {
        if (day1TaskCanvasRef.current == null) return
        if (day1Task2 == null) return
        const canvas = day1TaskCanvasRef.current
        const context = canvas.getContext('2d')
        if (context == null) return

        drawTask2Starter(context, day1Task2, fps)

    }, [day1Task2Sample])

    return (
        <Grid width="100%">
            <Typography variant="h3">Task 2</Typography>
            <canvas id="canvas_2_example" width="1000" height={(day1Task2Sample?.length + 2) * 20} ref={day1TaskSampleCanvasRef}></canvas>
            <Divider />
            <canvas id="canvas_2_solution" width="1000" height={(day1Task2?.length + 2) * 20} ref={day1TaskCanvasRef}></canvas>
        </Grid>
    )
}

const stringNumberMap = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}

const drawTask2Starter = (context: CanvasRenderingContext2D, day1TaskInput: string[], fps: number = 1) => {
    // Drawing for task1Sample
    let day1Solution: number[][] = []
    drawTask2(context, day1TaskInput, day1Solution)
    const wordsPattern = Object.keys(stringNumberMap).join('|');
    const lookaheadPattern = `(?=(${wordsPattern})|$)`;
    const stringRegex = new RegExp(`${lookaheadPattern}${lookaheadPattern}`, 'g')

    day1TaskInput.forEach((row, index) => {
        let numberMatches = Array.from(row.matchAll(/(\d+)/g))


        let firstNumberMatch: number;
        let lastNumberMatch: number;


        if (numberMatches.length === 0) {
            firstNumberMatch = 9000
            lastNumberMatch = -9000
        } else {
            if (numberMatches.length === 1) {
                firstNumberMatch = numberMatches[0].index
                lastNumberMatch = numberMatches[0].index + numberMatches[0][0].length - 1;
            } else {
                firstNumberMatch = numberMatches[0].index;
                lastNumberMatch = numberMatches[numberMatches.length - 1].index + numberMatches[numberMatches.length - 1][0].length - 1;
            }
        }

        let stringMatches = Array.from(row.matchAll(stringRegex)).filter((match) => match[1] != null)
        let firstStringMatch: number;
        let firstStringMatchWord: string;
        let lastStringMatch: number;
        let lastStringMatchWord: string;

        if (stringMatches.length === 0) {
            firstStringMatch = 9000
            lastStringMatch = -9000
        } else {
            if (stringMatches.length === 1) {
                firstStringMatch = stringMatches[0].index
                firstStringMatchWord = stringMatches[0][1]
                lastStringMatch = stringMatches[0].index + stringMatches[0][0].length - 1;
                lastStringMatchWord = stringMatches[0][1]
            } else {
                firstStringMatch = stringMatches[0].index;
                firstStringMatchWord = stringMatches[0][1]
                lastStringMatch = stringMatches[stringMatches.length - 1].index + stringMatches[stringMatches.length - 1][0].length - 1;
                lastStringMatchWord = stringMatches[stringMatches.length - 1][1]
            }
        }

        const firstInt = Math.min(firstNumberMatch, firstStringMatch)
        const lastInt = Math.max(lastNumberMatch, lastStringMatch)

        console.log(row, firstInt, lastInt)

        if (firstInt == null || lastInt == null) return row
        const localSolution = [...day1Solution, [firstNumberMatch, lastNumberMatch, firstStringMatch, firstStringMatchWord, lastStringMatch, lastStringMatchWord]]
        day1Solution = [...localSolution]
        setTimeout(() => {
            drawTask2(context, day1TaskInput, localSolution)
        }, (1000 / fps) * index)
    })
}

const getValues = (row, firstNumberMatch, lastNumberMatch, firstStringMatch, firstStringMatchWord, lastStringMatch, lastStringMatchWord) => {
    let firstNumber: number;
    let firstNumberType: 'number' | 'string'
    let lastNumber: number;
    let lastNumberType: 'number' | 'string'

    if (firstNumberMatch < firstStringMatch) {
        firstNumber = parseInt(row[firstNumberMatch])
        firstNumberType = 'number'
    } else {
        firstNumber = stringNumberMap[firstStringMatchWord]
        firstNumberType = 'string'
    }

    if (lastNumberMatch > lastStringMatch) {
        lastNumber = parseInt(row[lastNumberMatch])
        lastNumberType = 'number'
    } else {
        if (lastStringMatchWord == null) {
            lastNumber = firstNumber
            lastNumberType = firstNumberType
        } else {
            lastNumber = stringNumberMap[lastStringMatchWord]
            lastNumberType = 'string'
        }
    }

    return [firstNumber, lastNumber, firstNumberType, lastNumberType]
}

const drawTask2 = (context: CanvasRenderingContext2D, day1TaskInput: string[], day1Solution: number[][]) => {
    context.fillStyle = "#232332"
    let rollingSum = 0
    day1TaskInput.forEach((line, index) => {
        if (day1Solution[index] == null) return
        const values = getValues(line, day1Solution[index][0], day1Solution[index][1], day1Solution[index][2], day1Solution[index][3], day1Solution[index][4], day1Solution[index][5])
        const sum = parseInt(`${values[0]}${values[1]}`)
        rollingSum += sum
    })
    context.clearRect(0, 0, context.canvas.width, 20)
    drawText(context, `Day 1 Task 2 - sum: ${rollingSum}`, 0)

    if (day1Solution.length === 0) {
        day1TaskInput.forEach((line, index) => {
            drawText(context, line, 20 + index * 20)
        })
        return
    }

    const index = day1Solution.length - 1
    const line = day1TaskInput[index]
    context.clearRect(0, 20 + (index) * 20, context.canvas.width, 20)

    const values = getValues(line, day1Solution[index][0], day1Solution[index][1], day1Solution[index][2], day1Solution[index][3], day1Solution[index][4], day1Solution[index][5])

    const valueOne = values[0]
    const valueTwo = values[1]
    const sum = parseInt(`${valueOne}${valueTwo}`)

    const lineToPrint = `${line}: ${valueOne} + ${valueTwo} = ${sum}`

    const sumCharacterIndexes = []
    for (let i = 0; i < sum.toString().length; i++) {
        sumCharacterIndexes.push(lineToPrint.length - 1 - i)
    }

    const highlightCharacterIndexes = []
    if (values[2] === 'string') {
        [...Array(day1Solution[index][3].length)].forEach((_, i) => {
            highlightCharacterIndexes.push(day1Solution[index][2] + i)
        })
    } else {
        highlightCharacterIndexes.push(day1Solution[index][0])
    }

    if (values[3] === 'string') {
        [...Array(day1Solution[index][5].length)].forEach((_, i) => {
            highlightCharacterIndexes.push(day1Solution[index][4] + 1 + i)
        })
    } else {
        highlightCharacterIndexes.push(day1Solution[index][1])
    }

    drawText(context, lineToPrint, 20 + index * 20, highlightCharacterIndexes, sumCharacterIndexes)

    if (day1TaskInput.length === day1Solution.length) {
        const lineToPrint = `Solution: ${rollingSum}`

        const sumCharacterIndexes = []
        for (let i = 0; i < rollingSum.toString().length; i++) {
            sumCharacterIndexes.push(lineToPrint.length - 1 - i)
        }

        drawText(context, lineToPrint, 20 + day1TaskInput.length * 20, [], sumCharacterIndexes)
    }
}

export default Day0102