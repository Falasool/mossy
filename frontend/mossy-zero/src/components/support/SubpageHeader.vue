<script setup lang="ts">
    import { computed } from 'vue'
    import { NFlex, NButton, NIcon, NPopover, NDivider } from 'naive-ui'
    import { useRoute, useRouter } from 'vue-router'
    import { ChevronBack, ShareSocial, EllipsisHorizontal, HandRight, Warning } from '@vicons/ionicons5'
    import { useI18n } from 'vue-i18n'
    import { notyf } from '@/utils/notyf'
    import { useUserStateStore } from '@/stores/userStateStore'
    import { useThemeStore } from '@/stores/themeStore'


    interface Props {
        pageCategory: 'user' | 'activity' | 'tag'
    }

    const userStateStore = useUserStateStore()
    const props = defineProps<Props>();
    const route = useRoute()
    const router = useRouter()
    const theme = useThemeStore()
    const { t } = useI18n()
    const uri = route.params.id
    const bgcolor = computed(() => {
        return theme.isDarkMode ? "bg-neutral-700/70" : "bg-neutral-50/70"
    })

    const handleShare = async () => {
        if (navigator.share) {
            try {
                // TODO: Add shareable content
                await navigator.share({
                    title: '',
                    text: '',
                    url: ''
                })
            } catch (error) {
                notyf.error(t('ui.header.statusmsg.shareFail'))
            }
        } else {
            notyf.error(t('ui.header.statusmsg.shareApiNotSupported'));
        }
    }

    const handleBlock = async () => {
        if (!userStateStore.isLoggedIn) {
            notyf.error(t('ui.common_desc.loginMust'))
            return
        }
        // TODO: Add block functionality
    }

    const handleReport = async () => {
        if (!userStateStore.isLoggedIn) {
            notyf.error(t('ui.common_desc.loginMust'))
            return
        }
        // TODO: Add report functionality
    }
</script>

<template>
    <n-flex justify="space-between"
        class="z-40 px-2 sticky top-12 font-bold bg-opacity-30 backdrop-filter backdrop-blur-md h-12 items-center border-solid border-0 border-b border-gray-500"
        :class="bgcolor">
        <div class="w-2/12 text-left">
            <n-button icon-placement="left" circle :bordered="false" @click="router.back()">
                <template #icon>
                    <n-icon>
                        <ChevronBack />
                    </n-icon>
                </template>
                <!-- {{ t('ui.common_desc.go_back') }} -->
            </n-button>
        </div>
        <div class="w-7/12 text-center">
            {{ uri }}
        </div>
        <div class="w-2/12 text-right">
            <n-popover trigger="click" placement="bottom">
                <template #trigger>
                    <n-button icon-placement="right" circle :bordered="false">
                        <template #icon>
                            <n-icon>
                                <EllipsisHorizontal />
                            </n-icon>
                        </template>
                        <!-- {{ t('ui.common_desc.go_back') }} -->
                    </n-button>
                </template>
                <n-flex vertical class="putThemOnLeft">
                    <n-button icon-placement="left" text strong @click="handleShare">
                        <template #icon>
                            <n-icon>
                                <ShareSocial />
                            </n-icon>
                        </template>
                        {{ t('ui.common_desc.share') }}{{ t('ui.common_desc.person') }}
                    </n-button>
                    <n-button type="warning" icon-placement="left" text strong @click="handleBlock">
                        <template #icon>
                            <n-icon>
                                <HandRight />
                            </n-icon>
                        </template>
                        {{ t('ui.common_desc.block') }}
                    </n-button>
                    <n-button type="error" icon-placement="left" text strong @click="handleReport">
                        <template #icon>
                            <n-icon>
                                <Warning />
                            </n-icon>
                        </template>
                        {{ t('ui.common_desc.report') }}
                    </n-button>
                </n-flex>
            </n-popover>
        </div>
    </n-flex>
</template>

<style scoped>
    .putThemOnLeft button {
        text-align: left;
        width: fit-content;
    }
</style>