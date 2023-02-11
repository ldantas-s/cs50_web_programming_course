const followEvent = async (user_id) => {
    const data = await fetch(`/follow/${user_id}`)

    return await data.json()    
}

document.addEventListener('DOMContentLoaded', function() {
    const followButton = document.getElementById('follow-button')
    const followersCount = document.getElementById('followers-count')
    const followingCount = document.getElementById('following-count')
    
    followButton.addEventListener('click', function() {
        const userId = this.dataset.userid
        console.log(userId)
        followEvent(userId).then(data => {
            this.innerHTML = data.label_button
            followersCount.innerText = data.followers
            followingCount.innerTest = data.followers
        })
    })
})