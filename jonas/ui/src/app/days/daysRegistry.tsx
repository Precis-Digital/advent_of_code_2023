import { ReactElement } from "react";
import Day0101 from "./Day0101";
import Day0102 from "./Day0102";

export const DAYS_REGISTRY: { [x: string]: { [x: string]: ReactElement } } = {
  "01": {
    "01": <Day0101 />,
    "02": <Day0102 />
  }
};
