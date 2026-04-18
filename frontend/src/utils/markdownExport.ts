import type { ProjectDocument } from '../types/domain'

function sanitizeFileName(value: string) {
  return value
    .trim()
    .replace(/[\\/:*?"<>|]/g, '-')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '')
}

function triggerDownload(filename: string, content: string) {
  const blob = new Blob([content], { type: 'text/markdown;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')

  link.href = url
  link.download = filename
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}

export function exportDocumentAsMarkdown(projectName: string, document: ProjectDocument) {
  const safeProjectName = sanitizeFileName(projectName || 'b4vc-project')
  const safeKind = sanitizeFileName(document.kind)
  const filename = `${safeProjectName}-${safeKind}.md`
  const content = document.content || `# ${document.title}\n\n文档尚未生成。`

  triggerDownload(filename, content)
}

export function exportAllDocumentsAsMarkdown(projectName: string, documents: ProjectDocument[]) {
  documents
    .filter((document) => document.content)
    .forEach((document, index) => {
      window.setTimeout(() => {
        exportDocumentAsMarkdown(projectName, document)
      }, index * 150)
    })
}
