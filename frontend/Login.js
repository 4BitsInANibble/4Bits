import { StatusBar } from 'expo-status-bar';
import { SafeAreaView, ScrollView, StyleSheet, Text, View } from 'react-native';
import React, { Component } from 'react';
import { Appbar, BottomNavigation, FAB, useTheme, Searchbar } from 'react-native-paper';
import {useSafeAreaInsets, SafeAreaProvider} from 'react-native-safe-area-context';


const BOTTOM_APPBAR_HEIGHT = 80;
const MEDIUM_FAB_HEIGHT = 56;

const LoginScreen = () =>{
    return(
        <SafeAreaView style={styles.login}>
            <Text>Login Screen</Text>
        </SafeAreaView>

    ) 
    
}


const styles = StyleSheet.create({
    login: {
      flex: 1,
      justifyContent: 'center',
      alignItems: 'center'
    }
  });