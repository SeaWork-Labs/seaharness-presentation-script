import { createHash } from 'node:crypto'
import { mkdir, readFile, rename, unlink, writeFile } from 'node:fs/promises'
import { dirname, join } from 'node:path'

export async function sha256File(path) {
  return createHash('sha256').update(await readFile(path)).digest('hex')
}

export async function atomicReplace(dest, data, expectedSha) {
  if (expectedSha !== undefined) {
    try {
      const current = await sha256File(dest)
      if (current !== expectedSha) {
        console.error(`sha256 conflict: ${current} != ${expectedSha}`)
        process.exit(2)
      }
    } catch (error) {
      if (error && typeof error === 'object' && 'code' in error && error.code !== 'ENOENT') throw error
    }
  }
  await mkdir(dirname(dest), { recursive: true })
  const tmp = join(dirname(dest), `.${process.pid}.${Date.now()}.tmp`)
  try {
    await writeFile(tmp, data)
    await rename(tmp, dest)
  } catch (error) {
    await unlink(tmp).catch(() => undefined)
    throw error
  }
}
