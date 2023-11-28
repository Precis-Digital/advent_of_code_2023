import React from 'react'
import { DAYS_REGISTRY } from '../days/daysRegistry'
import { Grid } from '@mui/material'

export default function Page({ params }: { params: { dayNum: string } }) {
    const dayComponent = DAYS_REGISTRY[params.dayNum]

    return (
        <Grid container spacing={4} width="100%" height="100%" padding="5%" alignItems="center">
            <Grid item>
                <div>Day {params.dayNum}</div>
                {dayComponent != null ? dayComponent : <div>Not found</div>}
            </Grid>
        </Grid>
    )
}