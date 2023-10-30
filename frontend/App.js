import { StatusBar } from 'expo-status-bar';
import { SafeAreaView, ScrollView, StyleSheet, Text, View } from 'react-native';
import React, { Component } from 'react';

export default function App() {
  return (
  <SafeAreaView style={styles.container}>
    <View style={styles.toolbarView}></View>
    <ScrollView style={styles.buttonListView}></ScrollView>
  </SafeAreaView>
    // <View style={styles.container}>
    //   <Text>Nibble</Text>
    //   <StatusBar backgroundColor = "#16a085" animated = {true}/>
    // </View>
  );


}

// const Toolbar = () => {
//   return <SafeAreaView style={styles.container}>
//     <View style={styles.toolbarView}></View>
//   </SafeAreaView>
// }

const styles = StyleSheet.create({
  // container: {
  //   flex: 1,
  //   backgroundColor: '#f5f5dc',
  //   alignItems: 'center',
  //   justifyContent: 'center',
  // },
  toolbarView: {
    width: 340,
    height: 66,
    backgroundColor: 'white',
    shadowColor: 'grey',
    shadowOffset: {width: 0, height: 8},
    shadowOpacity: 0.4,
    shadowRadius: 10,
    borderRadius: 12,
    marginHorizontal: 24,
    marginVertical: 40,
  },
  buttonListView:{
    position='absolute',
    height: 66,
    width= '100%',
    marginHorizontal: 24,
    marginVertical: 40,
  }
});