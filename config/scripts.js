// utils.js
class NoteLoader {
    constructor(containerId, jsonDir) {
        this.containerId = containerId;
        this.jsonDir = jsonDir;
        this.notesContainer = document.getElementById(containerId);

        if (!this.notesContainer) {
            console.error(`Error: '${containerId}' element not found in the DOM.`);
            return;
        }
    }

    async loadAndRenderNotes() {
        const jsonFiles = await this.fetchJSONFiles();
        jsonFiles.forEach((note) => {
            const noteHTML = this.generateNoteHTML(note);
            this.notesContainer.insertAdjacentHTML('beforeend', noteHTML);
        });
    }

    async fetchJSONFiles() {
        const jsonFiles = [];
        const fileListResponse = await fetch(`${this.jsonDir}/file_list.txt`);
        const fileListText = await fileListResponse.text();
        const fileNames = fileListText.split('\n').filter(Boolean); // 去除空行

        for (const fileName of fileNames) {
            const fileResponse = await fetch(`${this.jsonDir}/${fileName}`);
            const fileContent = await fileResponse.json();
            jsonFiles.push(...fileContent);
        }

        return jsonFiles;
    }

    generateNoteHTML(note) {
        throw new Error("Must be implemented by subclass.");
    }
}

// diary-html.js
class DiaryLoader extends NoteLoader {
    generateNoteHTML(note) {
        const metadata = note.metadata;
        const content = note.content_html;

        return `
            <div class="container-content">
                <div class="data">${metadata.date}</div>
                <p>${content}</p>
            </div>
        `;
    }
}

// skill-text.js
class SkillLoader extends NoteLoader {
    generateNoteHTML(note) {
        const filename = note.filename;
        const metadata = note.metadata;
        const content = note.content_html;

        return `
            <div class="container-content">
                <div class="filename">${filename}</div>
                <p>${content}</p>
            </div>
        `;
    }
}

// main.js
function loadNotes(containerId, jsonDir, LoaderClass) {
    const container = document.getElementById(containerId);
    if (container) {
        const loader = new LoaderClass(containerId, jsonDir);
        loader.loadAndRenderNotes();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    loadNotes('container-diary', 'diary_json', DiaryLoader);
    loadNotes('container-skill', 'skill_json', SkillLoader);
});
