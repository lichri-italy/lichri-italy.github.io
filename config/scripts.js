function loadScript(url) {
    var script = document.createElement('script');
    script.setAttribute('type', 'text/javascript');
    script.setAttribute('src', url);
    document.getElementsByTagName('head')[0].appendChild(script);
}

// ========================================================= //

function loadAndDisplayPosts(containerId) {
    // 读取 JSON 文件
    fetch('../config/list_post.json')
        .then(response => response.json())
        .then(data => {
            // 按 last_modified_time 排序
            data.sort((a, b) => new Date(b.last_modified_time) - new Date(a.last_modified_time));

            // 获取指定容器元素
            const archiveList = document.getElementById(containerId);

            if (!archiveList) {
                console.error(`Element with id "${containerId}" not found.`);
                return;
            }

            // 初始化显示的条目数量
            let displayedItems = 10;
            let totalItems = data.length;

            // 显示前10个条目
            displayItems(data, archiveList, displayedItems);

            // 滚动事件监听器
            window.addEventListener('scroll', () => {
                const scrollPosition = window.scrollY + window.innerHeight;
                const documentHeight = document.body.offsetHeight;

                // 如果滚动到页面底部，加载更多条目
                if (scrollPosition >= documentHeight * 0.9) {
                    displayedItems = Math.min(displayedItems + 5, totalItems);
                    displayItems(data, archiveList, displayedItems);
                }
            });

            // 显示指定数量的条目
            function displayItems(data, archiveList, count) {
                // 清空现有条目
                archiveList.innerHTML = '';

                // 遍历数据并生成链接
                data.slice(0, count).forEach(post => {
                    const fileName = post.filename;
                    const filePath = post.file_path;
                    const date = post.last_modified_time.split('T')[0];
                    const textContent = post.text_content + '...';

                    const postItem = document.createElement('div');
                    postItem.className = 'post-item';

                    const linkParagraph = document.createElement('p');
                    const link = document.createElement('a');
                    link.href = filePath;
                    link.textContent = fileName;
                    linkParagraph.appendChild(link);

                    const dateElement = document.createElement('p');
                    dateElement.textContent = `发布日期: ${date}`;

                    const contentElement = document.createElement('p');
                    contentElement.textContent = textContent;

                    postItem.appendChild(linkParagraph);
                    postItem.appendChild(dateElement);
                    postItem.appendChild(contentElement);

                    archiveList.appendChild(postItem);
                });
            }
        })
        .catch(error => console.error('Error:', error));
}