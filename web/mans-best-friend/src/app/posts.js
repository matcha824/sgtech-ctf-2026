function buildPostHTML(post) {
    const imageHTML = post.image ? `<div class="post-image"><img src="${post.image}"></div>` : '';
    return `<div class="card post-card">
        <div class="post-header">
            <div class="post-avatar gradient-avatar">${post.authorAvatar}</div>
            <div class="post-meta">
                <strong>${post.author}</strong>
                <span>${post.timestamp}</span>
            </div>
        </div>
        <p class="post-text">${post.text}</p>
        ${imageHTML}
        <div class="post-stats">
            <span id="like-count-${post.id}">${post.likes.reactions} &nbsp;${post.likes.count} likes</span>
        </div>
    </div>`;
}

const POSTS_DATA = [
    {
        id: 1,
        author: 'Jill Smith',
        authorAvatar: '🐶',
        timestamp: "2 hours ago",
        text: "My favorite teacher ever!",
        image: "static/Teacher.png",
        likes: { count: 25, reactions: "👍❤️😂" },
    },
    {
        id: 2,
        author: 'Jill Smith',
        authorAvatar: '🐶',
        timestamp: "5 hours ago",
        text: "Happy anniversary to my parents!",
        image: "static/Parents.png",
        likes: { count: 101, reactions: "👍❤️😂" },
    },
    {
        id: 3,
        author: 'Jill Smith',
        authorAvatar: '🐶',
        timestamp: "2 days ago",
        text: "Born and raised in Chicago! Go Bears!",
        image: "static/Chicago.png",
        likes: { count: 67, reactions: "👍❤️😂" },
    },
    {
        id: 4,
        author: 'Jill Smith',
        authorAvatar: '🐶',
        timestamp: "3 days ago",
        text: "Happy birthday to my childhood dog!",
        image: "static/Dog.png",
        likes: { count: 70, reactions: "👍❤️😂" },
    },
    {
        id: 5,
        author: 'Jill Smith',
        authorAvatar: '🐶',
        timestamp: "3 days ago",
        text: "Got my first car! A 2020 Volkswagen!",
        image: "static/Car.png",
        likes: { count: 40, reactions: "👍❤️😂" },
    }
]

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('right-col').innerHTML = POSTS_DATA.map(buildPostHTML).join('');
})