import { Card, CardContent, Grid, Link } from '@mui/material'
import './global.css'
import { DAYS_REGISTRY } from './days/daysRegistry'

export default function Home() {
  return (
    <Grid container spacing={4} width="100%" height="100%" padding="5%" alignItems="center">
      {Array.from(Array(25).keys()).map((day) => {
        const paddedDate = (day + 1).toString().padStart(2, '0')
        return (
          <Grid item key={day} xs={6} m={4} xl={3} margin={0}>
            {DAYS_REGISTRY[paddedDate] != null ? (
              <Link href={`/${paddedDate}`}>
                <Card>
                  <CardContent>
                    Day {paddedDate}
                  </CardContent>
                </Card>
              </Link>
            ) : (
              <Card>
                <CardContent sx={{ color: 'grey' }}>
                  Day {paddedDate}
                </CardContent>
              </Card>
            )
            }
          </Grid>
        )
      })}
    </Grid>
  )
}
