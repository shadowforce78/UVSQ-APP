module.exports = {
    packagerConfig: {},
    rebuildConfig: {},
    makers: [
        {
            name: '@electron-forge/maker-zip',
            platforms: ['darwin', 'win32', 'linux'],
        },
        {
            name: '@electron-forge/maker-deb',
            config: {},
        },
    ],
    plugins: [
        [
            'electron-forge-build-tools',
            {
                android: {
                    keystore: {
                        // Remplis avec tes infos pour signer l'APK
                        path: './my-release-key.jks',
                        alias: 'my-key-alias',
                        password: 'my-key-password',
                    },
                },
            },
        ],
    ],
};
