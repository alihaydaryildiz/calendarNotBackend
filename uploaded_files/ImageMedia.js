import React, { useEffect, useState } from "react";
import { StyleSheet, View, ScrollView, SafeAreaView, TouchableOpacity, Modal, Dimensions, Text } from 'react-native';
import { Image } from 'expo-image';
import * as MediaLibrary from 'expo-media-library';
import PagerView from 'react-native-pager-view';

const { width, height } = Dimensions.get('screen');

const ImageMedia = () => {
    const [selectedImage, setSelectedImage] = useState([]);
    const [viewedImageIndex, setViewedImageIndex] = useState(0);
    const [modalVisibleStatus, setModalVisibleStatus] = useState(false);

    useEffect(() => {
        async function getImageMedia() {
            const { status } = await MediaLibrary.requestPermissionsAsync();
            if (status === 'granted') {
                const imageAssets = await MediaLibrary.getAssetsAsync({
                    mediaType: "photo",
                    first: 100,
                });
                setSelectedImage(imageAssets.assets);
            }
        }
        getImageMedia();
    }, []);

    const showModalFunction = (visible, index) => {
        setViewedImageIndex(index);
        setModalVisibleStatus(visible);
    };

    return (
        <SafeAreaView style={styles.container}>
            <ScrollView>
                <View style={styles.ImageContainer}>
                    {selectedImage.map((imaj, index) => (
                        <TouchableOpacity
                            key={index}
                            onPress={() => showModalFunction(true, index)}
                        >
                            <Image
                                style={styles.image}
                                source={{ uri: imaj.uri }}
                                contentFit="contain"
                            />
                        </TouchableOpacity>
                    ))}
                </View>

                {!!modalVisibleStatus && (
                    <Modal
                        transparent={false}
                        animationType="slide"
                        visible={modalVisibleStatus}
                        onRequestClose={() => setModalVisibleStatus(false)}
                    >
                        <View style={styles.modalContainer}>
                            <PagerView
                                style={styles.pagerView}
                                initialPage={viewedImageIndex}
                            >
                                {selectedImage.map((image, index) => (
                                    <View key={index} style={styles.page}>
                                        <Image
                                            source={{ uri: image.uri }}
                                            style={styles.fullImageStyle}
                                            contentFit="contain"
                                        />
                                    </View>
                                ))}
                            </PagerView>

                            <TouchableOpacity
                                style={styles.closeButtonStyle}
                                onPress={() => setModalVisibleStatus(false)}
                            >
                                <Text style={styles.closeButtonText}>Kapat</Text>
                            </TouchableOpacity>
                        </View>
                    </Modal>
                )}
            </ScrollView>
        </SafeAreaView>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#ffffff',
    },
    ImageContainer: {
        flexDirection: 'row',
        flexWrap: 'wrap',
        justifyContent: 'space-between',
    },
    image: {
        width: 100,
        height: 100,
        margin: 5,
        borderRadius: 10,
    },
    modalContainer: {
        flex: 1,
        backgroundColor: 'black',
    },
    pagerView: {
        width: width,
        height: height,
    },
    page: {
        justifyContent: 'center',
        alignItems: 'center',
    },
    fullImageStyle: {
        width: '100%',
        height: '100%',
    },
    closeButtonStyle: {
        position: 'absolute',
        top: 50,
        right: 20,
        padding: 10,
        backgroundColor: 'rgba(255, 255, 255, 0.5)',
        borderRadius: 5,
    },
    closeButtonText: {
        color: 'black',
        fontWeight: 'bold',
    },
});

export default ImageMedia;
