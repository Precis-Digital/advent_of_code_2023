"use client"
import React, { ReactElement, useEffect } from 'react'
import { Divider, Grid, Typography } from '@mui/material'
import { useRouter, useSearchParams } from 'next/navigation'

const Day0101 = (): ReactElement => {
    const day1TaskCanvasRef = React.useRef<HTMLCanvasElement>(null)
    const [day1Task1, setDay1Task1] = React.useState<string[] | undefined>(undefined)
    const day1TaskSampleCanvasRef = React.useRef<HTMLCanvasElement>(null)
    const [day1Task1Sample, setDay1Task1Sample] = React.useState<string[] | undefined>(undefined)
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
                setDay1Task1(data.data.split('\n'))
            })
        })

        fetch('/api/files/Day01_1_sample').then((resp) => {
            resp.json().then(data => {
                setDay1Task1Sample(data.data.split('\n'))
            })
        })
    }, [])

    useEffect(() => {
        if (day1TaskSampleCanvasRef.current == null) return
        if (day1Task1Sample == null) return
        const canvas = day1TaskSampleCanvasRef.current
        const context = canvas.getContext('2d')
        if (context == null) return

        drawTask1Starter(context, day1Task1Sample, fps)

    }, [day1Task1Sample])

    useEffect(() => {
        if (day1TaskCanvasRef.current == null) return
        if (day1Task1 == null) return
        const canvas = day1TaskCanvasRef.current
        const context = canvas.getContext('2d')
        if (context == null) return

        drawTask1Starter(context, day1Task1, fps)

    }, [day1Task1Sample])

    return (
        <Grid width="100%">
            <Typography variant="h3">Task 1</Typography>
            <canvas id="canvas_1_example" width="1000" height={(day1Task1Sample?.length + 2) * 20} ref={day1TaskSampleCanvasRef}></canvas>
            <Divider />
            <canvas id="canvas_1_solution" width="1000" height={(day1Task1?.length + 2) * 20} ref={day1TaskCanvasRef}></canvas>
        </Grid>
    )
}

const drawTask1Starter = (context: CanvasRenderingContext2D, day1TaskInput: string[], fps: number = 1) => {
    // Drawing for task1Sample
    let day1Solution: number[][] = []
    drawTask1(context, day1TaskInput, day1Solution)

    day1TaskInput.forEach((row, index) => {
        let numberMatches = Array.from(row.matchAll(/(\d+)/g))
        if (row === "425six14two46") {
            console.log(numberMatches)
            console.log(numberMatches[0][0])
        }

        let firstInt: number;
        let lastInt: number;

        if (numberMatches.length === 1) {
            firstInt = numberMatches[0].index
            lastInt = numberMatches[0].index + numberMatches[0][0].length - 1;
        } else {
            firstInt = numberMatches[0].index;
            lastInt = numberMatches[numberMatches.length - 1].index + numberMatches[numberMatches.length - 1][0].length - 1;
        }

        if (firstInt == null || lastInt == null) return row
        const localSolution = [...day1Solution, [firstInt, lastInt]]
        day1Solution.push([firstInt, lastInt])
        setTimeout(() => {
            drawTask1(context, day1TaskInput, localSolution)
        }, (1000 / fps) * index)
    })
}
const drawTask1 = (context: CanvasRenderingContext2D, day1TaskInput: string[], day1Solution: number[][]) => {

    context.fillStyle = "#232332"
    let rollingSum = 0
    day1TaskInput.forEach((line, index) => {
        if (day1Solution[index] == null) return
        const indexOne = line[day1Solution[index][0]]
        const indexTwo = line[day1Solution[index][1]]
        const sum = parseInt(`${indexOne}${indexTwo}`)
        rollingSum += sum
    })
    context.clearRect(0, 0, context.canvas.width, 20)
    drawText(context, `Day 1 Task 1 - sum: ${rollingSum}`, 0)

    if (day1Solution.length === 0) {
        day1TaskInput.forEach((line, index) => {
            drawText(context, line, 20 + index * 20)
        })
        return
    }

    const index = day1Solution.length - 1
    const line = day1TaskInput[index]
    context.clearRect(0, 20 + (index) * 20, context.canvas.width, 20)

    const indexOne = day1Solution[index][0]
    const indexTwo = day1Solution[index][1]
    const valueOne = line[indexOne]
    const valueTwo = line[indexTwo]
    const sum = parseInt(`${valueOne}${valueTwo}`)

    const lineToPrint = `${line}: ${valueOne} + ${valueTwo} = ${sum}`

    const sumCharacterIndexes = []
    for (let i = 0; i < sum.toString().length; i++) {
        sumCharacterIndexes.push(lineToPrint.length - 1 - i)
    }

    drawText(context, lineToPrint, 20 + index * 20, [indexOne, indexTwo], sumCharacterIndexes)

    if (day1TaskInput.length === day1Solution.length) {
        const lineToPrint = `Solution: ${rollingSum}`

        const sumCharacterIndexes = []
        for (let i = 0; i < rollingSum.toString().length; i++) {
            sumCharacterIndexes.push(lineToPrint.length - 1 - i)
        }

        drawText(context, lineToPrint, 20 + day1TaskInput.length * 20, [], sumCharacterIndexes)
    }
}

export const drawText = (context: CanvasRenderingContext2D, text: string, y: number, highlights: number[] = [], strongs: number[] = []) => {
    const fontSize = 12
    context.font = `${fontSize}px Arial`

    let currentXPos = 0

    text.split('').forEach((char, index) => {
        if (highlights.includes(index)) {
            context.fillStyle = "#FF0000"
        } else {
            context.fillStyle = "#232332"
        }

        if (strongs.includes(index)) {
            context.font = `bold ${fontSize}px Arial`
        } else {
            context.font = `${fontSize}px Arial`
        }

        let yPos = y + fontSize
        context.fillText(char, currentXPos, yPos)

        currentXPos += context.measureText(char).width
    })
}

export default Day0101