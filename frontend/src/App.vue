<template>

  <div class="layout">


    <aside class="sidebar">

      <h1>
        🚀 LifeOS
      </h1>


      <nav>

        <router-link to="/dashboard">
          🏠 首页
        </router-link>


        <router-link to="/profile">
          👤 个人档案
        </router-link>


        <router-link to="/daily">
          📝 每日记录
        </router-link>


        <router-link to="/goals">
          🎯 目标
        </router-link>


        <router-link to="/analysis">
          📊 数据分析
        </router-link>


        <router-link to="/ai">
          🤖 AI助手
        </router-link>


      </nav>


    </aside>



    <main class="content">

      <router-view />

    </main>


  </div>


</template>



<style>


.layout{

display:flex;

min-height:100vh;

}



.sidebar{

width:240px;

padding:30px;

background:#1f2937;

color:white;

}



.sidebar h1{

font-size:28px;

}



nav{

display:flex;

flex-direction:column;

gap:20px;

margin-top:40px;

}



nav a{

color:white;

text-decoration:none;

font-size:18px;

}



.content{

flex:1;

padding:40px;

background:#f5f6f8;

}


</style>