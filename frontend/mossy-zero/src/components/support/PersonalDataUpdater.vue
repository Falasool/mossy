<script setup lang="ts">
    import { ref, onMounted, inject } from 'vue'
    import type { Ref } from 'vue'
    import { NForm, NFormItem, NImage, NFlex, NInput, NUpload, NUploadDragger, NIcon, NDynamicInput, NSkeleton } from 'naive-ui';
    import { useLoadingBar } from 'naive-ui'
    import { FileTray } from '@vicons/ionicons5'
    import { useI18n } from 'vue-i18n';
    import type {
        UploadOnChange,
        FormRules,
        UploadFileInfo
    } from 'naive-ui'
    import { notyf } from '@/utils/notyf';
    import { callMossyApi, type MossyApiError } from '@/utils/apiCall';

    interface Avatar {
        file_content: string;
        file_type: string;
        file_size: number;
    }

    interface Header {
        file_content: string;
        file_type: string;
        file_size: number;
    }

    interface Field {
        name: string;
        value: string;
    }

    interface FormData {
        display_name: string;
        desc: string;
        avatar: Avatar;
        header: Header;
        fields: Field[];
    }

    const defaultFormData: FormData = {
        display_name: "",
        desc: "",
        avatar: {
            file_content: "",
            file_type: "",
            file_size: 0
        },
        header: {
            file_content: "",
            file_type: "",
            file_size: 0
        },
        fields: []
    };
    const { t } = useI18n()
    const loadingBar = useLoadingBar()
    const formData = inject<Ref<FormData>>('formData', ref(defaultFormData));
    const loading = inject<Ref<boolean>>('loading', ref(false));

    const formDisabled = ref(false)
    const rules: FormRules = {}

    const handleAvatar: UploadOnChange = (payload) => {
        if (payload.fileList.length != 0) {
            const listedFile = payload.fileList.pop()
            if (listedFile == undefined) {
                return
            }
            const file = listedFile.file as File
            if (file.size > 5 * 1024 * 1024) {
                notyf.error(t('ui.pages.settings.personal.basic_info.avatar.file_too_large'));
                return
            }

            const reader = new FileReader();

            reader.onload = (event) => {
                const base64String = (event.target?.result as string).split(',')[1];
                formData.value.avatar = {
                    "file_content": base64String,
                    "file_type": file.type,
                    "file_size": file.size
                };
            };

            reader.onerror = (error) => {
                console.error("Error reading file:", error);
            };

            reader.readAsDataURL(file);
        }
    }

    const handleHeader: UploadOnChange = (payload) => {
        if (payload.fileList.length != 0) {
            const listedFile = payload.fileList.pop()
            if (listedFile == undefined) {
                return
            }
            const file = listedFile.file as File
            if (file.size > 10 * 1024 * 1024) {
                notyf.error(t('ui.pages.settings.personal.basic_info.header.file_too_large'));
                return;
            }

            const reader = new FileReader();

            reader.onload = (event) => {
                const base64String = (event.target?.result as string).split(',')[1];
                formData.value.header = {
                    "file_content": base64String,
                    "file_type": file.type,
                    "file_size": file.size
                };
            };

            reader.onerror = (error) => {
                console.error("Error reading file:", error);
            };

            reader.readAsDataURL(file);
        }
    }

    const onCreate = () => {
        return { name: '', value: '' }
    }

    function debounce<T extends (...args: any[]) => void>(func: T, wait: number): (...args: Parameters<T>) => void {
        let timeout: ReturnType<typeof setTimeout> | undefined;
        return (...args: Parameters<T>): void => {
            if (timeout !== undefined) {
                clearTimeout(timeout);
            }
            loadingBar.start()
            timeout = setTimeout(() => {
                func(...args);
            }, wait);
        };
    }


    const submit = async () => {
        formDisabled.value = true
        await callMossyApi({
            method: 'POST',
            endpoint: '/api/m1/user/profile',
            data: formData.value
        }).then((response) => {
            formData.value = response
            notyf.success(t('ui.pages.settings.personal.basic_info.submit_success'))
            loadingBar.finish()
        }).catch(() => {
            notyf.error(t('ui.pages.settings.personal.basic_info.submit_failed'))
            loadingBar.error()
        }).finally(() => {
            formDisabled.value = false
        })
    }

    const debouncedSubmit = debounce(submit, 3000);
</script>
<template>
    <p>{{ t('ui.pages.settings.personal.basic_info.note') }}</p>
    <n-form :model="formData" size="large" @change="debouncedSubmit" :disabled="formDisabled">
        <n-form-item path="display_name">
            <template #label>
                <p class="p-0 m-0 font-bold text-base">{{ t('ui.pages.settings.personal.basic_info.display_name.label')
                    }}</p>
                <p class="p-0 m-0">{{ t('ui.pages.settings.personal.basic_info.display_name.instruction') }}</p>
            </template>
            <n-skeleton v-if="loading" :sharp="false" size="large" />
            <n-input v-else v-model:value="formData.display_name"
                :placeholder="t('ui.pages.settings.personal.basic_info.display_name.placeholder')" show-count
                :maxlength="30" clearable />
        </n-form-item>
        <n-form-item path="desc">
            <template #label>
                <p class="p-0 m-0 font-bold text-base">{{ t('ui.pages.settings.personal.basic_info.desc.label')
                    }}</p>
                <p class="p-0 m-0">{{ t('ui.pages.settings.personal.basic_info.desc.instruction', {
                    user: '@其他人', tag:
                        '#标签'
                }) }}</p>
            </template>
            <n-skeleton v-if="loading" :sharp="false" size="large" />
            <n-input v-else v-model:value="formData.desc"
                :placeholder="t('ui.pages.settings.personal.basic_info.desc.placeholder')" type="textarea"
                :autosize="{ minRows: 3 }" show-count :maxlength="500" clearable />
        </n-form-item>
        <n-form-item path="avatar">
            <template #label>
                <p class="p-0 m-0 font-bold text-base">{{ t('ui.pages.settings.personal.basic_info.avatar.label')
                    }}</p>
                <p class="p-0 m-0">{{ t('ui.pages.settings.personal.basic_info.avatar.instruction') }}</p>
            </template>
            <n-skeleton v-if="loading" :sharp="false" size="large" />
            <n-upload v-else :show-preview-button="true" :default-upload="false" list-type="image" :max="1"
                accept="image/*" v-model:value="formData.avatar" @change="handleAvatar">
                <n-upload-dragger>
                    <div v-if="formData.avatar.file_content == ''">
                        <n-icon size="32">
                            <FileTray />
                        </n-icon>
                        <p class="p-0 m-0 font-bold text-base">{{ t('ui.common_desc.drag_to_upload') }}</p>
                        <p class="p-0 m-0">{{ t('ui.pages.settings.personal.basic_info.avatar.placeholder') }}</p>
                    </div>
                    <div v-else>
                        <n-image :width="300" preview-disabled
                            :src="`data:${formData.avatar.file_type};base64,${formData.avatar.file_content}`" />
                        <div>
                            <p class="p-0 m-0 font-bold text-base">
                                {{ t('ui.pages.settings.personal.basic_info.avatar.instruction_for_replace') }}
                            </p>
                            <p class="p-0 m-0">
                                {{ t('ui.pages.settings.personal.basic_info.avatar.placeholder') }}
                            </p>
                        </div>
                    </div>
                </n-upload-dragger>
            </n-upload>
        </n-form-item>
        <n-form-item path="header">
            <template #label>
                <p class="p-0 m-0 font-bold text-base">{{ t('ui.pages.settings.personal.basic_info.header.label')
                    }}</p>
                <p class="p-0 m-0">{{ t('ui.pages.settings.personal.basic_info.header.instruction') }}</p>
            </template>
            <n-skeleton v-if="loading" :sharp="false" size="large" />
            <n-upload v-else :show-preview-button="true" :default-upload="false" list-type="image" :max="2"
                accept="image/*" v-model:value="formData.avatar" @change="handleHeader">
                <n-upload-dragger>
                    <div v-if="formData.header.file_content == ''">
                        <n-icon size="32">
                            <FileTray />
                        </n-icon>
                        <p class="p-0 m-0 font-bold text-base">{{ t('ui.setup_page.server_banner.instruction') }}</p>
                        <p class="p-0 m-0">{{ t('ui.pages.settings.personal.basic_info.header.placeholder') }}</p>
                    </div>
                    <div v-else>
                        <n-image :width="300" preview-disabled
                            :src="`data:${formData.header.file_type};base64,${formData.header.file_content}`" />
                        <div>
                            <p class="p-0 m-0 font-bold text-base">
                                {{ t('ui.pages.settings.personal.basic_info.header.instruction_for_replace') }}
                            </p>
                            <p class="p-0 m-0">
                                {{ t('ui.pages.settings.personal.basic_info.header.placeholder') }}
                            </p>
                        </div>
                    </div>
                </n-upload-dragger>
            </n-upload>
        </n-form-item>
        <n-form-item path="fields">
            <template #label>
                <p class="p-0 m-0 font-bold text-base">{{ t('ui.pages.settings.personal.basic_info.fields.label')
                    }}</p>
                <p class="p-0 m-0">{{ t('ui.pages.settings.personal.basic_info.fields.instruction') }}</p>
            </template>
            <n-skeleton v-if="loading" :sharp="false" size="large" />
            <n-dynamic-input v-else v-model:value="formData.fields" :max="6" :on-create="onCreate">
                <template #default="{ value }">
                    <n-input v-model:value="value.name" type="text"
                        :placeholder="t('ui.pages.settings.personal.basic_info.fields.placeholder_left')" />
                    <n-input v-model:value="value.value" type="text"
                        :placeholder="t('ui.pages.settings.personal.basic_info.fields.placeholder_right')" />
                </template>
            </n-dynamic-input>
        </n-form-item>
    </n-form>
</template>