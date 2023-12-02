import { promises as fs } from "fs";
export const dynamic = "force-dynamic"; // defaults to force-static
export async function GET(
  request: Request,
  { params }: { params: { dayNum: string } }
) {
  const fileContent = (
    await fs.readFile(process.cwd() + `/src/app/api/files/${params.dayNum}.txt`)
  ).toString();

  return Response.json({ data: fileContent });
}
