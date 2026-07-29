<template>
  <div class="slidev-layout ac-split h-full flex flex-col">
    <div><slot /></div>
    <div class="slide-body">
      <div class="grid grid-cols-2">
        <div class="pr-8"><slot name="left" /></div>
        <div class="pl-8 border-l border-[#DADEE6]"><slot name="right" /></div>
      </div>
    </div>
  </div>
</template>
